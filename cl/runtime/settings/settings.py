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

from abc import abstractmethod
from dataclasses import MISSING
from dataclasses import dataclass

from dotenv import load_dotenv, find_dotenv
from dynaconf import Dynaconf
from typing import Any, Type, ClassVar
from typing import Dict
from typing_extensions import Self

# Load dotenv first (override priority is envvars, dotenv, Dynaconf)
load_dotenv()

# Dynaconf settings in raw format (including system settings), some keys may be strings instead of dictionaries or lists
_all_settings = Dynaconf(
    environments=True,
    envvar_prefix="CL",
    env_switcher="CL_SETTINGS_ENV",
    envvar="CL_SETTINGS_FILE",
    settings_files=["settings.toml", ".secrets.toml"],
    dotenv_override=True,
)

# Extract user settings only using as_dict(), then convert containers at all levels to dictionaries and lists
# and convert root level keys to lowercase in case the settings are specified using envvars in uppercase format
_user_settings = {k.lower(): v for k, v in _all_settings.as_dict().items()}

dynaconf_envvar_prefix = _all_settings.envvar_prefix_for_dynaconf
"""Environment variable prefix for overriding dynaconf file settings."""

dynaconf_file_patterns = _all_settings.settings_file
"""List of Dynaconf settings file patterns or file paths."""

dynaconf_loaded_files = _all_settings._loaded_files  # noqa
"""Loaded dynaconf settings files."""

dynaconf_root_path = _all_settings._root_path # noqa
"""Environment variable prefix for overriding dynaconf file settings."""


@dataclass(slots=True, kw_only=True)
class Settings:
    """Base class for a singleton settings object."""

    __settings_dict: ClassVar[Dict[Type, Settings]] = {}
    """Dictionary of initialized settings objects indexed by the the settings class type."""

    @classmethod
    @abstractmethod
    def get_prefix(cls) -> str | None:
        """
        Dynaconf fields will be filtered by 'prefix_' before being passed to the settings class constructor.
        If None is returned, all fields will be passed in which case the settings class constructor must
        accept or ignore unknown fields.

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

            # Validate prefix if not None
            if prefix is not None:
                prefix_description = f"Dynaconf settings prefix '{prefix}' returned by '{cls.__name__}.get_prefix()'"
                if prefix == "":
                    raise RuntimeError(f"{prefix_description} is an empty string, use None instead.")
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

            if prefix is None:
                # Prefix is None, use system settings and extract required keys only
                # This will exclude fields that are not specified in the settings class
                settings_dict = {k: getattr(_all_settings, k, None) for k in dir(_all_settings) if k in required_fields}
            else:
                # Filter user settings by 'prefix_' and create a new dictionary where prefix is removed from keys
                # This will include fields that are not specified in the settings class
                p = prefix + "_"
                settings_dict = {k[len(p):]: v for k, v in _user_settings.items() if k.startswith(p)}

                # Check for missing required fields
                missing_fields = [k for k in required_fields if k not in settings_dict]
                if missing_fields:
                    # Combine the global Dynaconf envvar prefix with settings prefix in uppercase
                    envvar_prefix = f"{dynaconf_envvar_prefix}_{prefix.upper()}"
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
                    if dynaconf_loaded_files:
                        dynaconf_file_list = dynaconf_loaded_files
                    else:
                        dynaconf_file_patterns_str = ", ".join(dynaconf_file_patterns)
                        dynaconf_file_list = [f"No {dynaconf_file_patterns_str} files in default search path"]
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

            result = cls(**settings_dict)
            cls.__settings_dict[cls] = result

        return result
