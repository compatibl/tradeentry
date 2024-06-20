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

import importlib
import inspect
from collections import Counter
from pkgutil import walk_packages
from types import ModuleType

from cl.runtime.schema.type_decl import TypeDecl, pascalize
from cl.runtime.schema.type_decl_key import TypeDeclKey
from memoization import cached
from typing import Dict, List, Iterable
from typing import Type
from typing_extensions import Self


def is_record(record_type):
    """Return true if the type is a record based on the presence of 'get_key' method."""
    return (
            inspect.isclass(record_type) and
            hasattr(record_type, "get_key") and
            callable(getattr(record_type, "get_key")) and
            not inspect.isabstract(record_type) and
            not record_type.__name__.endswith("Mixin")
    )


class Schema:
    """
    Provide declarations for the specified type and all dependencies.
    """

    @classmethod
    @cached
    def get_types(cls) -> Iterable[Type]:
        """Get all types found in the list of packages specified in settings."""
        return cls.get_type_dict().values()

    @classmethod
    @cached
    def get_type_by_short_name(cls, short_name: str) -> Type:
        """Get type from short name (class name with optional package alias)."""

        # Get dictionary of types indexed by alias
        type_dict_by_short_name = cls.get_type_dict()

        # TODO: Update to support short name with namespace prefix
        record_type = type_dict_by_short_name.get(short_name, None)
        if record_type is None:
            raise RuntimeError(f"Record class with short name {short_name} is not found "
                               f"in the list of packages specified in settings.")
        return record_type

    @classmethod
    @cached
    def get_type_by_class_path(cls, class_path: str) -> Type:
        """Get type from full class path in module.ClassName format."""

        # Get dictionary of types indexed by alias
        type_dict_by_class_path = cls.get_type_dict_by_class_path()

        # TODO: Update to support short name with namespace prefix
        record_type = type_dict_by_class_path.get(class_path, None)
        if record_type is None:
            raise RuntimeError(f"Record class with class path {class_path} is not found "
                               f"in the list of packages specified in settings.")
        return record_type

    @classmethod
    @cached
    def get_type_dict_by_class_path(cls) -> Dict[str, Type]:
        """Get a dictionary of types using full class path in module.ClassName format as key."""

        # Get record types from the dictionary of types by short name
        record_types = cls.get_type_dict().values()

        # Create the dictionary of types by class path
        result = {f"{record_type.__module__}.{record_type.__name__}": record_type for record_type in record_types}
        return result

    @classmethod
    @cached
    def get_type_dict(cls) -> Dict[str, Type]:
        """Get a dictionary of types using short name (class name with optional package alias) as key."""

        # TODO: Load from config file
        packages = ["cl.runtime", "stubs.cl.runtime"]

        # Get modules for the specified packages
        modules = cls._get_modules(packages)

        # Get record types by iterating over modules
        record_types = set(
            record_type for module in modules for name, record_type in inspect.getmembers(module, is_record)
        )

        # Ensure names are unique
        # TODO: Support namespace aliases to resolve conflicts
        record_names = [record_type.__name__ for record_type in record_types]

        # Check that there are no repeated names, report errors if there are
        if len(set(record_names)) != len(record_names):
            # Count the occurrences of each name in the list
            record_name_counts = Counter(record_names)

            # Find names that are repeated more than once
            repeated_names = [record_name for record_name, count in record_name_counts.items() if count > 1]

            # Report repeated names
            package_names_str = ", ".join(packages)
            repeated_names_str = ", ".join(repeated_names)
            raise RuntimeError(f"The following class names in the list of packages {package_names_str} "
                               f"are repeated more than once: {repeated_names_str}")

        # Create result dict
        result = dict(zip(record_names, record_types))
        return result

    @classmethod
    def for_key(cls, key: TypeDeclKey) -> Self:
        """Create or return cached object for the specified type declaration key."""
        class_path = f"{key[1][1]}.{key[2]}"  # TODO: Use parse_key method
        return cls.for_class_path(class_path)

    @classmethod
    def for_class_path(cls, class_path: str) -> Dict[str, Dict]:
        """Create or return cached object for the specified class path in module.ClassName format."""

        record_type = cls.get_type_by_class_path(class_path)
        return cls.for_type(record_type)

    @classmethod
    @cached
    def for_type(cls, record_type: Type) -> Dict[str, Dict]:
        """
        Declarations for the specified type and all dependencies, returned as a dictionary.

        Args:
            record_type: Type of the record for which the schema is created.
        """
        dependencies = set()
        type_decl_obj = TypeDecl.for_type(record_type, dependencies=dependencies)
        old_size = 0
        new_size = 1
        while new_size > old_size:
            old_size = len(dependencies)
            for dependency_type in dependencies:
                TypeDecl.for_type(dependency_type, dependencies=dependencies)
            new_size = len(dependencies)
        type_decl_list = [type_decl_obj] + list(dependencies)

        # TODO: Move pascalize to a helper class
        result = {
            pascalize(f"{type_decl.module[1]}.{type_decl.name}"): type_decl.to_type_decl_dict()
            for type_decl in type_decl_list
        }
        return result

    @classmethod
    @cached
    def _get_modules(cls, packages: List[str]) -> List[ModuleType]:
        """
        Get a list of ModuleType objects for submodules at all levels of the specified packages or root modules.
        Args:
            packages: List of packages or root module strings in dot-delimited format, for example ['cl.runtime']
        """
        result = []
        for package in packages:
            # Import root module of the package
            root_module = importlib.import_module(package)
            result.append(root_module)  # Add the root module itself
            # Get module info for all submodules, note the trailing period added as per walk_packages documentation
            for module_info in walk_packages(root_module.__path__, root_module.__name__ + "."):
                module_name = module_info.name
                # Import the submodule using its full name
                submodule = importlib.import_module(module_name)
                result.append(submodule)
        return result
