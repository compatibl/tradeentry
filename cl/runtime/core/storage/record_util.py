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

import sys
from functools import cache
from importlib import import_module
from typing import TypeVar, List, Tuple

T = TypeVar("T")


class RecordUtil:
    """Helper methods for Record."""

    @staticmethod
    @cache
    def get_class(module_path: str, class_name: str) -> T:
        """Get class from module name and class name.

        Args:
            module_path: Dot-delimited Python module path.
            class_name: Top-level class name without delimiters.

        Notes:
            This method caches its return value and is only called once for each combination of arguments.
        """

        if '.' in class_name:
            raise RuntimeError(f"Class name {class_name} is dot-delimited. "
                               f"Only top-level class names without delimiter can be stored.")

        # Check that the module exists and is fully initialized
        module = sys.modules.get(module_path)
        module_spec = getattr(module, "__spec__", None) if module is not None else None
        module_initializing = getattr(module_spec, "_initializing", False) if module_spec is not None else None
        module_imported = module_initializing is False  # To ensure it is not another value evaluating to False

        # Import dynamically if not already imported, report error if not found
        if not module_imported:
            try:
                module = import_module(module_path)
            except ModuleNotFoundError:
                raise RuntimeError(f"Module {module_path} is not found when loading class {class_name}.")

        # Get class from module, report error if not found
        try:
            result = getattr(module, class_name)
            return result
        except AttributeError:
            raise RuntimeError(f"Module {module_path} does not contain top-level class {class_name}.")

    # TODO: Implement custom LRU caching
    @staticmethod
    def get_class_path(class_: T) -> str:
        """Returns the concatenation of module path and class name using dot delimiter.

        - The argument is either a class, e.g. StubClass, or a type variable obtained
          from class instance, e.g. type(stub_class_instance).
        """
        return f"{class_.__module__}.{class_.__name__}"

    @staticmethod
    @cache
    def split_class_path(class_path: str) -> Tuple[str]:
        """Split dot-delimited class path into module path and class name."""
        result_list = class_path.rsplit(".", 1)
        return tuple(result_list)

    # TODO: Implement custom LRU caching
    @staticmethod
    def get_inheritance_chain_paths(class_: T) -> List[str]:
        """Returns inheritance chain as the list of class path strings.

        - The result is in MRO order and excludes abstract base classes.
        - The argument is either a class, e.g. StubClass, or a type variable obtained
          from class instance, e.g. type(stub_class_instance).
        """

        # Include only those classes in MRO that implement get_root_class
        # These are the classes that can be queried from the database
        result = [
            f"{c.__module__}.{c.__name__}" for c in class_.mro() if getattr(c, "get_root_class", None) is not None
        ]

        if len(result) == 0:
            class_path = RecordUtil.get_class_path(class_)
            raise RuntimeError(f"To be stored in a data source, class {class_path} or its base must implement the "
                               f"static method get_root_class(). Its return value determines the database table "
                               f"where instances of this class and its bases are stored. For example, if B is "
                               f"inherited from A, then B.get_root_class() and A.get_root_class() both return A.")

        return result

