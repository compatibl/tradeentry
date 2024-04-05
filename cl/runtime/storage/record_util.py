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
import attrs
from importlib import import_module
from typing import List, Tuple, Type, Any, Dict
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
        """
        Returns the list of fully qualified class names in MRO order starting from this class
        and ending with the class that has suffix Key. Exactly one class with suffix Key should
        be present in MRO, error otherwise.
        """

        # Get the list of classes in MRO
        complete_mro = [f"{c.__module__}.{c.__name__}" for c in cls.mro()]

        # Find classes whose name has Key suffix in MRO list
        key_class_indices = [index for index, string in enumerate(complete_mro) if string.endswith('Key')]
        key_class_count = len(key_class_indices)

        # Make sure there is only one such class in the inheritance chain
        if key_class_count == 0:
            raise RuntimeError(f"Class {cls.__module__}.{cls.__name__} has no parent with suffix `Key`. "
                               "Add Key suffix to key class name or implement `KeyMixin` interface.")
        elif key_class_count > 1:
            raise RuntimeError(f"Class {cls.__module__}.{cls.__name__} has more than one parent with suffix `Key`. "
                               "Ensure only one class has suffix `Key` or implement `KeyMixin` interface.")

        # Truncate the inheritance chain to drop classes after the class with Key suffix
        key_class_index = key_class_indices[0]
        fully_qualified_names = complete_mro[:key_class_index+1]

        # TODO: Add package aliases
        # Remove module from fully qualified names
        result = [name.split('.')[-1] for name in fully_qualified_names]

        return result

    @staticmethod
    @cached(custom_key_maker=lambda cls: f"{cls.__module__}.{cls.__name__}")
    def get_table(cls: Type) -> str:
        """
        Name of the database table where records for this key is stored.

        By convention, table name consists of a namespace (full package path or short alias)
        followed by the dot delimiter and then the key class name without suffix Key.
        """

        # The last element of inheritance chain is the key class
        inheritance_chain = RecordUtil.get_inheritance_chain(cls)

        # Remove Key suffix if present, otherwise return the original name
        result = inheritance_chain[-1].removesuffix("Key")

        return result

    @staticmethod
    def get_key(obj: Any) -> str:
        """
        Key as string in semicolon-delimited string format without table name.

        For composite keys, the embedded keys are concatenated in the order of their declaration without brackets:

            - No primary key fields: '' (i.e. empty string)
            - One primary key field A: 'A'
            - Two primary key fields A and B: 'A;B'
            - Two primary key fields 'A1;A2' and 'B': 'A1;A2;B'
        """
        raise RuntimeError(f"Method get_key() for class {type(self).__name__} in module {type(self).__module__} "
                           f"is neither implemented in code nor by a decorator.")

    @staticmethod
    def get_generic_key(obj: Any) -> str:
        """
        Generic key string defines both the table and the record within the table. It consists of the
        table name followed by the primary key in semicolon-delimited string format.

        By convention, table name consists of a namespace (full package path or short alias) followed by
        the class name of the common base to all classes stored in the table with dot delimiter:

        - No primary key fields: 'namespace.RecordType'
        - One primary key field A: 'namespace.RecordType;A'
        - Two primary key fields A and B: 'namespace.RecordType;A;B'
        - Two primary key fields 'A1;A2' and 'B': 'namespace.RecordType;A1;A2;B'
        """
        return f"{RecordUtil.get_table(type(obj))};{RecordUtil.get_key(obj)}"

    @staticmethod
    def to_dict(obj: Any) -> Dict[str, Any]:
        """Serialize to dictionary containing other dictionaries, lists and primitive types."""

        # TODO: Add memoization
        cls = type(obj)
        if attrs.has(cls):
            return attrs.asdict(obj)
        else:
            raise RuntimeError(f"Class {cls.__module__}.{cls.__name__} does not use one of the supported frameworks "
                               f"(dataclasses, attrs, pydantic) and does not inherit from DataMixin or RecordMixin.")

    @staticmethod
    def from_dict(cls, data: Dict[str, Any]) -> Any:
        """Create an instance of cls from dictionary containing other dictionaries, lists and primitive types."""
        result = cls()
        for key, value in data.items():
            if key != "_t":
                setattr(result, key, value)
        return result
