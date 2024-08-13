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

from cl.runtime.serialization.sentinel_type import sentinel_value
from cl.runtime.settings.settings import Settings
from dataclasses import dataclass
from typing import Dict

_package_aliases_dict: Dict[str, str] = {}
"""Cached package aliases for faster lookup."""


@dataclass(slots=True, kw_only=True, frozen=True)
class ApiSettings:
    """REST API settings."""

    package_aliases: Dict[str, str] | None = None
    """
    Custom namespace package or code subdirectory aliases as a dictionary in 'module_prefix: alias' format.

    Notes:
        - Use this feature to (a) organize type lists and DB tables by alias prefix in large projects and
          (b) resolve conflicts when two or more record types share the same class name
        - When specified, alias.ClassName is used, otherwise ClassName is used without a prefix
        - The same alias applies to all subdirectories of 'module_prefix'
    """

    def get_package_alias(self, module_prefix: str) -> str | None:
        """Get alias for the module prefix in dot-delimited format or None if alias is not specified."""

        if self.package_aliases is None:
            # Return None and exit if package_aliases are not specified
            return None

        # Otherwise check if a cached value exists, using missing_value as sentinel
        if (alias := _package_aliases_dict.get(module_prefix, sentinel_value)) == sentinel_value:
            # Cached value is not found, scan package_aliases for a matching prefix
            alias = next((v for k, v in self.package_aliases.items() if module_prefix.startswith(k)), None)
            # Add to cache
            _package_aliases_dict[module_prefix] = alias

        return alias
