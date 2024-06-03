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

from cl.runtime.settings.config import dynaconf_settings
from dataclasses import dataclass
from typing import ClassVar
from typing import Dict


@dataclass(slots=True)
class ApiSettings:
    """REST API settings do not affect the UI."""

    __default: ClassVar[ApiSettings | None] = None
    """Default instance is initialized from Dynaconf settings."""

    package_aliases: Dict[str, str] | str | None = None
    """
    Optional package aliases for the REST API, and DB in 'pattern: alias' format.
    Use this feature to organize types by package in large projects and to
    resolve conflicts when classes in different modules share the same class name.
    - Usage:
        - When module does not match the glob pattern, ClassName is used without prefix
        - When module matches the glob pattern, alias.ClassName is used.
        - This setting has no effect where full module is required, e.g., for the _class field.
    - This REST API setting does not affect the UI
    - Dictionary or string in JSON format is accepted
    """

    @staticmethod
    def default() -> ApiSettings:
        """Default instance is initialized from Dynaconf settings."""

        if ApiSettings.__default is None:
            # Load from Dynaconf settings on first call
            api_settings_dict = dynaconf_settings["api_settings"]
            ApiSettings.__default = ApiSettings(**api_settings_dict)
        return ApiSettings.__default
