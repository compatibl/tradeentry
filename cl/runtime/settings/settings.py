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

from abc import abstractmethod
from dataclasses import MISSING
from dataclasses import dataclass
from dynaconf import Dynaconf
from typing import Any
from typing import Dict
from typing_extensions import Self

# Dynaconf settings in raw format (including system settings), some keys may be strings instead of dictionaries or lists
dynaconf_all_settings = Dynaconf(
    environments=True,
    envvar_prefix="CL",
    env_switcher="CL_SETTINGS_ENV",
    envvar="CL_SETTINGS_FILE",
    settings_files=["settings.toml", ".secrets.toml"],
)

dynaconf_envvar_prefix = dynaconf_all_settings.envvar_prefix_for_dynaconf
"""Environment variable prefix for overriding dynaconf file settings."""

dynaconf_loaded_files = dynaconf_all_settings._loaded_files  # noqa
"""Loaded dynaconf settings files."""

# Extract user settings only using as_dict(), then convert containers at all levels to dictionaries and lists
# and convert root level keys to lowercase in case the settings are specified using envvars in uppercase format
dynaconf_user_settings = {k.lower(): v for k, v in dynaconf_all_settings.as_dict().items()}

_settings_dict: Dict[str, "Settings"] = {}
"""Dictionary of preloaded settings objects indexed by the settings path."""


@dataclass(slots=True, kw_only=True, frozen=True)
class Settings:
    """Base class for a singleton settings object."""

    @classmethod
    @abstractmethod
    def get_prefix(cls) -> str:
        """
        Dynaconf field prefix for this settings class without the trailing underscore,
        for example 'runtime' for the Runtime package.

        Notes:
            - Only those config fields that start from the prefix are used by this settings class
            - The prefix is removed before the fields are provided to the constructor of this class
        """

    @classmethod
    def instance(cls) -> Self:
        """Return singleton instance."""

        # Each settings class has a unique prefix used to filter dynaconf fields
        prefix = cls.get_prefix()

        # Add underscore to prefix after checking it is not already included
        if prefix.endswith("_"):
            raise RuntimeError(f"Dynaconf settings prefix '{prefix}' must not end with underscore.")
        prefix = prefix + "_"

        # Check if cached value exists, load if not found
        if (result := _settings_dict.get(prefix, None)) is None:
            # List of required fields in cls (fields for which neither default nor default_factory is specified)
            required_fields = [
                name
                for name, field_info in cls.__dataclass_fields__.items()  # noqa
                if field_info.default is MISSING and field_info.default_factory is MISSING
            ]

            # Filter user settings by prefix and create a new dictionary where prefix is removed from keys
            settings_dict = {k[len(prefix) :]: v for k, v in dynaconf_user_settings.items() if k.startswith(prefix)}

            # Find required fields that are not specified
            missing_fields = [k for k in required_fields if k not in settings_dict]
            if missing_fields:
                # List loaded files for the error message
                if isinstance(dynaconf_loaded_files, str):
                    settings_file_str = dynaconf_loaded_files
                else:
                    settings_file_str = ", ".join(dynaconf_loaded_files)

                # Combine the global Dynaconf envvar prefix with settings prefix in uppercase
                envvar_prefix = f"{dynaconf_envvar_prefix}_{prefix.upper()}"

                # List of missing required fields
                fields_error_msg_list = [
                    f">>> '{envvar_prefix}{k.upper()}' (envvar/.env) or '{prefix}{k}' (Dynaconf)"
                    for k in missing_fields
                ]
                fields_error_msg_str = "\n".join(fields_error_msg_list)

                # Raise exception with detailed information
                raise ValueError(
                    f"Required fields not found in Dynaconf settings file(s): "
                    f"{settings_file_str}:\n" + fields_error_msg_str
                )

            result = cls(**settings_dict)
            _settings_dict[prefix] = result

        return result
