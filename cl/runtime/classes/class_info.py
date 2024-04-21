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

import attrs
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
            Tuple of module_path, class_name
        """
        result = class_path.rsplit(".", 1)
        return result[0], result[1]

    @staticmethod
    @cached
    def get_class_type(class_path: str) -> Type:
        """
        Get class type from string in `module.ClassName` format, importing the module if necessary.

        Notes:
            Return value is cached to increase performance.

        Args:
            class_path: String in module.ClassName format.
        """

        module_path, class_name = ClassInfo.split_class_path(class_path)

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
            if hasattr(c, "get_key")
            and callable(getattr(c, "get_key"))
            and not getattr(getattr(c, "get_key"), "__isabstractmethod__", False)
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

    @staticmethod
    @cached(custom_key_maker=lambda record_type: f"{record_type.__module__}.{record_type.__name__}")
    def get_key_type(record_type: Type) -> str:
        """
        Name of the database table where records for this key is stored.

        By convention, table name consists of a namespace (full package path or short alias)
        followed by the dot delimiter and then the key class name without suffix Key.
        """

        # The last element of inheritance chain is the key class
        inheritance_chain = ClassInfo.get_inheritance_chain(record_type)

        # Remove Key suffix if present, otherwise return the original name
        result = inheritance_chain[-1].removesuffix("Key")

        return result

    @staticmethod
    @cached(custom_key_maker=lambda record_type: f"{record_type.__module__}.{record_type.__name__}")
    def get_table(record_type: Type) -> str:
        """
        Name of the database table where records for this key is stored.

        By convention, table name consists of a namespace (full package path or short alias)
        followed by the dot delimiter and then the key class name without suffix Key.
        """

        # The last element of inheritance chain is the key class
        inheritance_chain = ClassInfo.get_inheritance_chain(record_type)

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
        raise RuntimeError(
            f"Method get_key() for class {type(obj).__name__} in module {type(obj).__module__} "
            f"is neither implemented in code nor by a decorator."
        )

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
        return f"{ClassInfo.get_table(type(obj))};{ClassInfo.get_key(obj)}"

    @staticmethod
    def pack(obj: Any) -> Dict[str, Any]:
        """Serialize to dictionary containing other dictionaries, lists and primitive types."""

        # TODO: Add memoization
        cls = type(obj)
        if attrs.has(cls):
            result = attrs.asdict(obj)
            result["_class"] = f"{cls.__module__}.{cls.__name__}"
            return result
        else:
            raise RuntimeError(
                f"Class {cls.__module__}.{cls.__name__} does not use one of the supported frameworks "
                f"(dataclasses, attrs, pydantic)."
            )

    @staticmethod
    def to_tuple_key(key_type: Type, record_or_key: Any) -> Tuple | None:
        """
        Convert all key formats to key dict.

        Notes:
            For composite keys, the embedded keys are represented as embedded dicts.

        Returns:
            Dict of key fields.

        Args:
            key_type: Type of key class.
            record_or_key: Record, key, dict, semicolon-delimited string, or None.
        """
        if record_or_key is None or isinstance(record_or_key, tuple):
            return record_or_key
        elif type(record_or_key) is key_type:
            field_types = get_type_hints(key_type)
            result = tuple(getattr(record_or_key, x) for x in field_types)
            return result
        else:
            raise RuntimeError(
                f"Cannot convert key object to tuple because its type `{type(record_or_key).__name__}` "
                f"is not the same as key type `{key_type.__name__}`."
            )

    @staticmethod
    def to_generic_key(key_type: Type, record_or_key: Any) -> Tuple | None:
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
        raise NotImplementedError()

    @staticmethod
    def _deserialize(class_type: Type, data: Dict[str, Any]) -> Any:  # TODO: Deprecated?
        """Create an instance of cls from dictionary containing other dictionaries, lists and primitive types."""

        if isinstance(data, dict):
            field_types = get_type_hints(class_type)
            return class_type(
                **{k: ClassInfo._deserialize(field_types[k], v) for k, v in data.items() if k != "_class"}
            )
        elif isinstance(data, list):
            return [ClassInfo._deserialize(class_type.__args__[0], item) for item in data]
        else:
            return data
