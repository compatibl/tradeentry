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
from dataclasses import dataclass
from dynaconf import Dynaconf
from typing import Dict
from typing_extensions import Self


def get_dynaconf_dict() -> Dict[str, Dict]:
    """Load dynaconf settings and convert them to hierarchical dictionary format."""

    # Dynaconf settings in raw format, some keys may be strings instead of dictionaries or lists
    raw_settings = Dynaconf(
        environments=True,
        envvar_prefix="CL",
        env_switcher="CL_SETTINGS_ENV",
        settings_files=["settings.yaml", ".secrets.yaml"],
        merge_enabled=True,
    )

    # Convert containers at all levels to dictionaries and lists
    result = raw_settings.as_dict()

    # Convert root level keys to lowercase in case the settings are
    # specified using environment variables in SETTINGS_KEY format
    result = {k.lower(): v for k, v in result.items()}

    return result


_dynaconf_dict: Dict[str, Dict] = get_dynaconf_dict()
"""The entire set of Dynaconf settings in hierarchical dictionary format."""

_settings_dict: Dict[str, Settings] = {}
"""Dictionary of preloaded settings objects indexed by the settings path."""


@dataclass(slots=True, kw_only=True, frozen=True)
class Settings:
    """Base class for a singleton settings object."""

    @classmethod
    @abstractmethod
    def get_prefix(cls) -> str:
        """
        Dynaconf field prefix for this settings class with the trailing underscore (if the underscore-delimited),
        for example 'runtime_' for the Runtime package.

        Notes:
            - Only those config fields that start from the prefix are used by this settings class
            - The prefix is removed before the fields are provided to the constructor of this class
        """

    @classmethod
    def instance(cls) -> Self:
        """Return singleton instance."""

        # Each settings class has a unique prefix used to filter dynaconf fields
        prefix = cls.get_prefix()

        # Check if cached value exists, load if not found
        if (result := _settings_dict.get(prefix, None)) is None:
            # Filter by prefix and create a new dictionary where prefix is removed from keys
            settings_dict = {k[len(prefix) :]: v for k, v in _dynaconf_dict.items() if k.startswith(prefix)}

            result = cls(**settings_dict)
            _settings_dict[prefix] = result

        return result
