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
import re
from dataclasses import dataclass, field
from fnmatch import fnmatch
from typing import Dict, ClassVar
from orjson import orjson
from cl.runtime.settings.config import dynaconf_settings


# Module pattern including lowercase letters and numbers, *, ?, [, ] with dot delimiter
pattern_regex_str = r"^([a-z0-9_\*\?\[\]]+\.)*[a-z0-9_\*\?\[\]]+$"
pattern_regex = re.compile(pattern_regex_str)

# Module including lowercase letters and numbers with dot delimiter
module_regex_str = r"^[a-z0-9_]+(\.[a-z0-9_]+)*$"
module_regex = re.compile(module_regex_str)

# Glob wildcard symbols including *, ?, and [
glob_regex_str = r"[\*\?\[]"
glob_regex = re.compile(glob_regex_str)


@dataclass(slots=True, init=False)
class PackageAliases:
    """
    Package aliases using namespace or module glob pattern.

    - Multiple patterns and namespaces can have the same alias.
    - If the key contains one or more wildcard symbols it is matched as a pattern, otherwise as a namespace.
    """

    __default: ClassVar[PackageAliases | None] = None
    """Default instance is initialized from settings and may be subsequently modified in code."""

    _exact_dict: Dict[str, str]
    """Keys in this dictionary must match the entire module string exactly."""

    _prefix_dict: Dict[str, str]
    """Keys in this dictionary must match module prefix."""

    _pattern_dict: Dict[str, str]
    """Keys in this dictionary are matched as a glob wildcard pattern."""

    def __init__(self, alias_dict: Dict[str, str] | str | None = None):
        """Initialize from dictionary of aliases where key is namespace or glob pattern and value is alias."""

        # Parse if dictionary is passed as string
        if isinstance(alias_dict, str):
            try:
                alias_dict = orjson.loads(alias_dict)
            except orjson.JSONDecodeError as e:
                raise RuntimeError(f"Error decoding this `package_aliases` string into JSON: {alias_dict}")
        elif not isinstance(alias_dict, dict):
            raise RuntimeError(f"Param `package_aliases` with type {type(alias_dict)} is neither dict nor JSON string")

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

        # Validate to detect when pattern is not suitable for a module string
        if not pattern_regex.match(pattern):
            raise RuntimeError(f"Package alias pattern {pattern} does not consist of dot-delimited lowercase "
                               f"letters and numbers with glob wildcard characters *?[].")

        if glob_regex.search(pattern):
            # Glob pattern
            self._pattern_dict[pattern] = alias
        else:
            # Match `namespace` exactly and `namespace.` as a prefix to avoid
            # having namespace a match module abc
            self._exact_dict[pattern] = alias
            self._prefix_dict[pattern + "."] = alias

    def get_alias(self, module: str) -> str | None:
        """Get alias for the module or None if alias is not set."""

        # Validate to detect when argument is not a module string
        if not module_regex.match(module):
            raise RuntimeError(f"Module {module} does not consist of dot-delimited lowercase letters or numbers.")

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

    @staticmethod
    def default() -> PackageAliases:
        """Default instance is initialized from settings and may be subsequently modified in code."""

        if PackageAliases.__default is None:
            # Load from configuration if not set
            PackageAliases.__default = PackageAliases(dynaconf_settings.package_aliases)
        return PackageAliases.__default
