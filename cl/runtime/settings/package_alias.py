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

from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.serialization.sentinel_type import sentinel_value
from cl.runtime.settings.package_alias_key import PackageAliasKey
from dataclasses import dataclass
from typing import Dict

_package_alias_dict: Dict[str, str] = {}
"""Cached package aliases with module as key for faster lookup."""


@dataclass(slots=True, kw_only=True)
class PackageAlias(PackageAliasKey, RecordMixin[PackageAliasKey]):
    """
    Custom package alias defined using module glob pattern.

    Notes:
        - When specified, alias.ClassName is used in storage and REST API, otherwise ClassName is used without a prefix
        - Use to resolve conflicts when multiple packages use the same class name
        - Use to organize types and DB tables by package in large projects
    """

    package_alias: str = missing()
    """When specified, alias.ClassName is used in storage and REST API, otherwise ClassName is used without a prefix."""

    def get_key(self) -> PackageAliasKey:
        return PackageAliasKey(package_pattern=self.package_pattern)

    @classmethod
    def get_package_alias(cls, module: str) -> str | None:
        """Get alias for the module in dot-delimited format or None if alias is not specified."""

        # Otherwise check if a cached value exists, using missing_value as sentinel
        if (alias := _package_alias_dict.get(module, sentinel_value)) == sentinel_value:
            # Cached value is not found, scan PackageAlias records for a matching prefix
            alias = None
            # TODO: next((v for k, v in self.package_aliases.items() if module_prefix.startswith(k)), None)
            # Add to cache
            _package_alias_dict[module] = alias

        return alias
