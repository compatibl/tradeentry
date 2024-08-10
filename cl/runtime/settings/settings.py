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
from functools import reduce

from typing_extensions import Self
from dataclasses import dataclass
from typing import Dict
from dynaconf import Dynaconf


def get_dynaconf_dict() -> Dict[str, Dict]:
    """Load dynaconf settings and convert them to hierarchical dictionary format."""

    # Dynaconf settings in raw format, some keys may be strings instead of dictionaries or lists
    raw_settings = Dynaconf(
        environments=True,
        envvar_prefix="CL",
        env_switcher="CL_CONFIG_ENV",
        settings_files=["settings.yaml", ".secrets.yaml"],
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
    def get_settings_path(cls) -> str:
        """Path relative to dynaconf settings file root in dot delimited format."""

    @classmethod
    def instance(cls) -> Self:
        """Return singleton instance."""

        # Each derived settings class defines a unique path
        settings_path = cls.get_settings_path()

        # Check if cached value exists, load if not found
        if (result := _settings_dict.get(settings_path, None)) is None:

            # Use dot-delimited settings path 'a.b' to access 'dynaconf_settings["a"]["b"]'
            settings_dict = reduce(lambda d, key: d[key], settings_path.split('.'), _dynaconf_dict)

            # TODO: Support hierarchical data using deserializer
            # TODO: Support JSON string format for fields
            result = cls(**settings_dict)
            _settings_dict[settings_path] = result

        return result
