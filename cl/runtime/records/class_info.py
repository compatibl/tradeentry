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
from abc import ABC
from importlib import import_module
from memoization import cached
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing import get_type_hints


class ClassInfo(ABC):
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
            Tuple of module_name, class_name
        """
        result = class_path.rsplit(".", 1)
        return result[0], result[1]

    @staticmethod
    @cached
    def get_class_type(class_path: str) -> Type:
        """
        Get class type from string in 'module.ClassName' format, importing the module if necessary.

        Notes:
            Return value is cached to increase performance.

        Args:
            class_path: String in module.ClassName format.
        """

        module_name, class_name = ClassInfo.split_class_path(class_path)

        # Check that the module exists and is fully initialized
        module = sys.modules.get(module_name)
        module_spec = getattr(module, "__spec__", None) if module is not None else None
        module_initializing = getattr(module_spec, "_initializing", False) if module_spec is not None else None
        module_imported = module_initializing is False  # To ensure it is not another value evaluating to False

        # Import dynamically if not already imported, report error if not found
        if not module_imported:
            try:
                module = import_module(module_name)
            except ModuleNotFoundError:
                raise RuntimeError(f"Module {module_name} is not found when loading class {class_name}.")

        # Get class from module, report error if not found
        try:
            result = getattr(module, class_name)
            return result
        except AttributeError:
            raise RuntimeError(f"Module {module_name} does not contain top-level class {class_name}.")

    @staticmethod
    @cached(custom_key_maker=lambda record_type: f"{record_type.__module__}.{record_type.__name__}")
    def get_inheritance_chain(record_type: Type) -> List[str]:
        """
        Returns the list of fully qualified class names in MRO order starting from this class
        and ending with the class that has suffix Key. Exactly one class with suffix Key should
        be present in MRO, error otherwise.
        """

        # Get the list of classes in MRO
        fully_qualified_names = [
            f"{c.__module__}.{c.__name__}"
            for c in record_type.mro()
            if hasattr(c, "get_key") and not c.__name__.endswith("Mixin")
        ]

        # Make sure there is only one such class in the inheritance chain
        if len(fully_qualified_names) == 0:
            raise RuntimeError(
                f"Class {record_type.__module__}.{record_type.__name__} does not implement get_key(self) method."
            )

        # TODO: Add package aliases
        # Remove module from fully qualified names
        result = [name.split(".")[-1] for name in fully_qualified_names]

        return result
