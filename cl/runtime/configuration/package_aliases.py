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

from dataclasses import dataclass, field
from fnmatch import fnmatch
from typing import Dict


@dataclass(slots=True, init=False)
class PackageAliases:
    """
    Package aliases using namespace or module glob pattern.

    - Multiple patterns and namespaces can have the same alias.
    - If the key contains one or more wildcard symbols it is matched as a pattern, otherwise as a namespace.
    """

    _exact_dict: Dict[str, str]
    """Keys in this dictionary must match the entire module string exactly."""

    _prefix_dict: Dict[str, str]
    """Keys in this dictionary must match module prefix."""

    _pattern_dict: Dict[str, str]
    """Keys in this dictionary are matched as a glob wildcard pattern."""

    def __init__(self, alias_dict: Dict[str, str] | None = None):
        """Initialize from dictionary of aliases where key is namespace or glob pattern and value is alias."""

        # Must initialize here if defining a custom init
        self._exact_dict = dict()
        self._prefix_dict = dict()
        self._pattern_dict = dict()

        # Read dictionary of aliases passed as a parameter
        if alias_dict is not None:
            for key, value in alias_dict.items():
                self.add_alias(key, value)

    def add_alias(self, pattern: str, alias: str) -> None:
        """
        Add alias for packages and modules that matches the pattern or namespace.

        - Multiple patterns and namespaces can have the same alias.
        - If the key contains one or more wildcard symbols it is matched as a pattern, otherwise as a namespace.
        """
        if '*' not in pattern and '?' not in pattern and '[' not in pattern:
            # Match `namespace` exactly and `namespace.` as a prefix to avoid
            # having namespace a match module abc
            self._exact_dict[pattern] = alias
            self._prefix_dict[pattern + "."] = alias
        else:
            # Glob pattern
            self._pattern_dict[pattern] = alias

    def get_alias(self, module: str) -> str | None:
        """Get alias for the module or None if alias is not set."""
        # Exact matches
        for exact, alias in self._exact_dict.items():
            if exact == module:
                return alias

        # Prefix matches
        for prefix, alias in self._prefix_dict.items():
            if module.startswith(prefix):
                return alias

        # Glob pattern matches
        for pattern, alias in self._pattern_dict.items():
            if fnmatch(module, pattern):
                return alias

        # No matches, return None
        return None
