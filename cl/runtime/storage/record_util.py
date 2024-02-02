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
from importlib import import_module
from typing import List, Tuple, Type
from memoization import cached


class RecordUtil:
    """Helper methods for Record."""

    @staticmethod
    def get_class_path(cls: Type) -> str:
        """Returns the concatenation of module path and class name using dot delimiter.

        - The argument cls is either a literal class type, for example StubClass,
          or a type variable obtained from a class instance, for example type(stub_class_instance).
        - This method is also used to calculate key for LRU caching of functions taking class
          as their argument. This method is itself not cached because caching would involve
          calling the same method, resulting in no performance gain.
        """
        return f"{cls.__module__}.{cls.__name__}"

    @staticmethod
    def split_class_path(class_path: str) -> Tuple[str, str]:
        """Split dot-delimited class path into module path and class name.

        Returns:
            Tuple of module_path, class_name
        """
        result = class_path.rsplit(".", 1)
        return result[0], result[1]

    @staticmethod
    @cached
    def get_class_type(module_path: str, class_name: str) -> Type:
        """Get class from module name and class name.

        Args:
            module_path: Dot-delimited Python module path.
            class_name: Top-level class name without delimiters.

        Notes:
            This method caches its return value and is only called once for each combination of arguments.
        """

        if '.' in class_name:
            raise RuntimeError(
                f"Class name {class_name} is dot-delimited. "
                f"Only top-level class names without delimiter can be stored."
            )

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

    @staticmethod
    @cached(custom_key_maker=lambda cls: f"{cls.__module__}.{cls.__name__}")
    def get_inheritance_chain(cls: Type) -> List[str]:
        """Returns inheritance chain as the list of class path strings.

        - The argument cls is either a literal class type, for example StubClass,
          or a type variable obtained from a class instance, for example type(stub_class_instance)
        - The result is in MRO order and includes only those classes that implement get_table()
        - Return value of get_table() must be the same for all classes in the inheritance chain.
        """

        # The list of base classes for which a polymorphic query can return this record.
        # It includes only those classes in MRO of this record that implement get_table()
        # method, and its return value must be the same for all of them.
        result = [
            f"{c.__module__}.{c.__name__}" for c in cls.mro() if RecordUtil.is_init_implemented(c)
        ]

        # TODO: Implement memoize
        if len(result) == 0:
            class_path = RecordUtil.get_class_path(cls)
            raise RuntimeError(
                f"To be stored in a data source, class {class_path} or its base must implement the method "
                f"get_table() returning the name of the table where records of this type are stored."
            )

        return result

    @staticmethod
    @cached(custom_key_maker=lambda cls: f"{cls.__module__}.{cls.__name__}")
    def is_init_implemented(cls: Type):
        """Return true if `init(self)` method is present and marked by _implemented."""

        method = getattr(cls, "init", None)
        return method is not None and getattr(method, "_implemented", False)
