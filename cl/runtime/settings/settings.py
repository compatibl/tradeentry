# Copyright (C) 2023-present The Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
import os
from abc import ABC
from abc import abstractmethod
from dataclasses import MISSING
from dataclasses import dataclass
from typing import ClassVar
from typing import Dict
from typing import Iterable
from typing import List
from typing import Type
from dotenv import find_dotenv
from dotenv import load_dotenv
from dynaconf import Dynaconf
from typing_extensions import Self
from cl.runtime.context.env_util import EnvUtil
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.records.record_util import RecordUtil
from cl.runtime.settings.project_settings import SETTINGS_FILES_ENVVAR
from cl.runtime.settings.project_settings import ProjectSettings

# Load dotenv first (the priority order is envvars first, then dotenv, then settings.yaml and .secrets.yaml)
load_dotenv()

# TODO: Use dash delimiter in standard OrderedUuid format instead of updating the format here
process_id = (
    OrderedUuid.to_readable_str(OrderedUuid.create_one())
    .replace(":", "-")
    .replace(".", "-")
    .replace("T", "-")
    .replace("Z", "")
)
"""Process timestamp is OrderedUuid in readable string format created during the Python process launch."""

# Determine if we are inside a test and store the result in a global variable for performance
is_inside_test = EnvUtil.is_inside_test()

# Select Dynaconf test environment when invoked from the pytest or UnitTest test runner.
# Other runners not detected automatically, in which case the Dynaconf environment must be
# configured in settings explicitly.
if is_inside_test:
    os.environ["CL_SETTINGS_ENV"] = "test"

_all_settings = Dynaconf(
    environments=True,
    envvar_prefix="CL",
    env_switcher="CL_SETTINGS_ENV",
    envvar=SETTINGS_FILES_ENVVAR,
    settings_files=[
        # Specify the exact path to prevent uncertainty associated with searching in multiple directories
        os.path.normpath(os.path.join(ProjectSettings.get_project_root(), "settings.yaml")),
        os.path.normpath(os.path.join(ProjectSettings.get_project_root(), ".secrets.yaml")),
    ],
    dotenv_override=True,
)
"""
Dynaconf settings in raw format (including system settings), some keys may be strings instead of dictionaries or lists.
"""

_user_settings = {k.lower(): v for k, v in _all_settings.as_dict().items()}
"""
Extract user settings only using as_dict(), then convert containers at all levels to dictionaries and lists
and convert root level keys to lowercase in case the settings are specified using envvars in uppercase format
"""

_dynaconf_envvar_prefix = _all_settings.envvar_prefix_for_dynaconf
"""Environment variable prefix for overriding dynaconf file settings."""

_dynaconf_file_patterns = _all_settings.settings_file
"""List of Dynaconf settings file patterns or file paths."""

# Convert to list if a single string is specified
if isinstance(_dynaconf_file_patterns, str):
    _dynaconf_file_patterns = [_dynaconf_file_patterns]

_dynaconf_loaded_files = _all_settings._loaded_files  # noqa
"""Loaded dynaconf settings files."""

_dynaconf_dir_path = _all_settings._root_path  # noqa
"""Absolute path the location of the first Dynaconf file if found, None otherwise."""

_dotenv_file_path = find_dotenv_output if (find_dotenv_output := find_dotenv()) != "" else None
"""Absolute path to .env file if found, None otherwise."""

_dotenv_dir_path = os.path.dirname(_dotenv_file_path) if _dotenv_file_path is not None else None
"""Absolute path to .env directory if found, None otherwise."""


@dataclass(slots=True, kw_only=True)
class Settings(ABC):
    """Base class for a singleton settings object."""

    __settings_dict: ClassVar[Dict[Type, Settings]] = {}
    """Dictionary of initialized settings objects indexed by the the settings class type."""

    @classmethod
    @abstractmethod
    def get_prefix(cls) -> str:
        """
        Dynaconf fields will be filtered by 'prefix_' before being passed to the settings class constructor.

        Notes:
            - The prefix must be lowercase
            - The prefix must not start or end with underscore but may include underscore separator(s)
            - The prefix is removed before the fields are provided to the constructor of this settings class
        """

    @classmethod
    def instance(cls) -> Self:
        """Return singleton instance."""

        # Check if cached value exists, load if not found
        if (result := cls.__settings_dict.get(cls, None)) is None:
            # A settings class may specify an optional prefix used to filter dynaconf fields
            prefix = cls.get_prefix()

            # Validate prefix
            prefix_description = f"Dynaconf settings prefix '{prefix}' returned by '{cls.__name__}.get_prefix()'"
            if prefix is None:
                raise RuntimeError(f"{prefix_description} is None.")
            if prefix == "":
                raise RuntimeError(f"{prefix_description} is an empty string.")
            if not prefix.islower():
                raise RuntimeError(f"{prefix_description} must be lowercase.")
            if prefix.startswith("_"):
                raise RuntimeError(f"{prefix_description} must not start with an underscore.")
            if prefix.endswith("_"):
                raise RuntimeError(f"{prefix_description} must not end with an underscore.")

            # List of required fields in cls (fields for which neither default nor default_factory is specified)
            required_fields = [
                name
                for name, field_info in cls.__dataclass_fields__.items()  # noqa
                if field_info.default is MISSING and field_info.default_factory is MISSING
            ]

            # Filter user settings by 'prefix_' and create a new dictionary where prefix is removed from keys
            # This will include fields that are not specified in the settings class
            p = prefix + "_"
            settings_dict = {k[len(p) :]: v for k, v in _user_settings.items() if k.startswith(p)}

            # Check for missing required fields
            missing_fields = [k for k in required_fields if k not in settings_dict]
            if missing_fields:
                # Combine the global Dynaconf envvar prefix with settings prefix in uppercase
                envvar_prefix = f"{_dynaconf_envvar_prefix}_{prefix.upper()}"
                dynaconf_msg = f"(in lowercase with prefix '{prefix}_')"
                envvar_msg = f"(in uppercase with prefix '{envvar_prefix}_')"

                # Environment variables
                sources_list = [f"Environment variables {envvar_msg}"]

                # Dotenv file or message that it is not found
                if (env_file := find_dotenv()) != "":
                    env_file_name = env_file
                else:
                    env_file_name = "No .env file in default search path"
                sources_list.append(f"Dotenv file {envvar_msg}: {env_file_name}")

                # Dynaconf file(s) or message that they are not found
                if _dynaconf_loaded_files:
                    dynaconf_file_list = _dynaconf_loaded_files
                else:
                    _dynaconf_file_patterns_str = ", ".join(_dynaconf_file_patterns)
                    dynaconf_file_list = [f"No {_dynaconf_file_patterns_str} file(s) in default search path"]
                sources_list.extend(f"Dynaconf file {dynaconf_msg}: {x}" for x in dynaconf_file_list)

                # Convert to string
                settings_sources_str = "\n".join(f"    - {x}" for x in sources_list)

                # List of missing required fields
                fields_error_msg_list = [
                    f"    - '{envvar_prefix}_{k.upper()}' (envvar/.env) or '{prefix}_{k}' (Dynaconf)"
                    for k in missing_fields
                ]
                fields_error_msg_str = "\n".join(fields_error_msg_list)

                # Raise exception with detailed information
                raise ValueError(
                    f"Required settings field(s) for {cls.__name__} not found:\n{fields_error_msg_str}\n"
                    f"Settings sources searched in the order of priority:\n{settings_sources_str}"
                )

            # TODO: Add a check for nested complex types in settings, if these are present deserialization will fail
            # TODO: Can custom deserializer that removes trailing and leading _ can be used without cyclic reference?
            result = cls(**settings_dict)

            # Invoke init method for each class hierarchy member from base to derived
            RecordUtil.init_all(result)

            # Cache the result
            cls.__settings_dict[cls] = result

        return result

    @classmethod
    def get_project_root(cls) -> str:  # TODO: Merge with the version from ProjectSettings
        """
        Returns absolute path of the directory containing .env file, and if not present the directory
        containing the first Dynaconf settings file found. Error message if neither is found.
        """
        if _dotenv_dir_path is not None:
            # Use .env file location if found
            return _dotenv_dir_path
        elif _dynaconf_dir_path is not None:
            # Otherwise use the location of the first Dynaconf file found
            # TODO: Add a test to confirm the logic when several Dynaconf files are in different locations
            return _dynaconf_dir_path
        else:
            raise RuntimeError(
                "Cannot get project root because neither .env file nor dynaconf settings file are found. "
                "Project root is defined based on the location of these two files (with .env having a priority)."
            )

    @classmethod
    def normalize_paths(cls, field_name: str, field_value: Iterable[str] | str | None) -> List[str]:
        """
        Convert to absolute path if path relative to the location of .env or Dynaconf file is specified
        and convert to list if single value is specified.
        """

        # Check that the argument is either None, a string or, an iterable
        if field_value is None:
            # Accept None and treat it as an empty list
            return []
        elif isinstance(field_value, str):
            paths = [field_value]
        elif hasattr(field_value, "__iter__"):
            paths = list(field_value)
        else:
            raise RuntimeError(
                f"Field '{field_name}' with value '{field_value}' in class '{cls.__name__}' "
                f"must be a string or an iterable of strings."
            )

        result = [cls.normalize_path(field_name, path) for path in paths]
        return result

    @classmethod
    def normalize_path(cls, field_name: str, field_value: str | None) -> str:
        """Convert to absolute path if path relative to the location of .env or Dynaconf file is specified."""

        if field_value is None or field_value == "":
            raise RuntimeError(f"Field '{field_name}' in class '{cls.__name__}' has an empty element.")
        elif isinstance(field_value, str):
            # Check that 'field_value' is a string
            result = field_value
        else:
            raise RuntimeError(
                f"Field '{field_name}' in class '{cls.__name__}' has an element "
                f"with type {type(field_value)} which is not a string."
            )

        if not os.path.isabs(result):
            project_root = cls.get_project_root()
            result = os.path.join(project_root, result)

        # Return as a normalized path string
        result = os.path.normpath(result)
        return result

