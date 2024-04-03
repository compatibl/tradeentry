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

import gc
import importlib
import inspect
import pkgutil
from abc import ABCMeta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Type, TypeVar, Union, get_type_hints

import attrs

from cl.runtime.primitive.string_util import to_pascal_case

T = TypeVar('T')


class Transform(str, Enum):
    """
    Enumeration for transformation types with predefined attributes.

    Attributes:
        attrs: Represents "__attrs_attrs__" transformation.
        dataclass: Represents "__dataclass_fields__" transformation.
    """

    attrs = "__attrs_attrs__"
    dataclass = "__dataclass_fields__"


# noinspection PyPep8Naming
class memoize(dict):
    """Simple dict-based cache decorator"""

    def __init__(self, func):
        super().__init__()
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


class ClassInfo:
    """Contain reflection based helper static methods."""

    __is_initialized: bool = False
    __data_types_map: Dict[str, type] = dict()
    # module_name: shortname
    __package_shortname_map: Dict[str, str] = dict()
    # shortname: module
    __shortname_package_map: Dict[str, str] = dict()

    @classmethod
    @property
    def package_shortname_map(cls) -> Dict[str, str]:
        """Get a copy of the mapping of module names to shortnames."""
        return cls.__package_shortname_map.copy()

    @staticmethod
    def register_shortname(module_name: str, shortname: str):
        """
        Register a shortname for a module.

        Parameters:
            module_name: The module name.
            shortname: The shortname to register.
        """
        ClassInfo.__package_shortname_map[module_name] = shortname
        ClassInfo.__shortname_package_map[shortname] = module_name
        ClassInfo.__add_shortname_related_types(module_name, shortname)

    @staticmethod
    def unregister_shortname(module_name: str):
        """
        Unregister a shortname for a module.

        Parameters:
            module_name: The module name to unregister.
        """
        shortname = ClassInfo.__package_shortname_map.pop(module_name)
        ClassInfo.__shortname_package_map.pop(shortname)
        ClassInfo.__remove_shortname_related_types(module_name, shortname)

    @staticmethod
    @memoize
    def get_derived_types(module_name: str, base_type: Type[T]) -> Set[Type[T]]:
        """Extract all derived classes from specified module."""
        try:
            module_ = importlib.import_module(module_name)
        except ImportError as error:
            raise Exception(f'Cannot import module: {error.name}. Check sys.path')

        derived_types: Set[Type[T]] = set()

        packages = list(pkgutil.walk_packages(path=module_.__path__, prefix=module_.__name__ + '.'))
        modules = [x for x in packages if not x.ispkg]
        for m in modules:
            try:
                m_imp = importlib.import_module(m.name)
            except SyntaxError as error:
                print(f'Cannot import module: {m.name}. Error: {error.msg}. Line: {error.lineno}, {error.offset}')
                continue
            except NameError as error:
                print(f'Cannot import module: {m.name}. Error: {error.args}')
                continue
            except ModuleNotFoundError as error:
                print(f'Cannot import module: {m.name}. Error: {str(error)}')
                continue
            classes = inspect.getmembers(m_imp, inspect.isclass)
            derived_types.update([x[1] for x in classes if base_type in x[1].__mro__])

        if base_type in derived_types:
            derived_types.remove(base_type)
        return derived_types

    @staticmethod
    def get_type(name: str) -> type:
        """Return data derived type given its name."""

        if not ClassInfo.__is_initialized or name not in ClassInfo.__data_types_map:
            # Try to update map one more time. This scenario is possible depending on
            # first call to get_type and which classes where imported at that moment.
            ClassInfo.__init_types()

            if name not in ClassInfo.__data_types_map:
                raise Exception(
                    f'Class {name} is not found in ClassInfo data types map. ' f'Import this class before loading.',
                )

        return ClassInfo.__data_types_map[name]

    @staticmethod
    def try_get_type(name: str) -> type:
        """Return data derived type given its name. Returns None if not found"""

        if not ClassInfo.__is_initialized:
            ClassInfo.__init_types()

        return ClassInfo.__data_types_map.get(name, None)

    @staticmethod
    @memoize
    def from_analyst_to_short_name(name: str) -> str:
        """
        Convert an analyst name to a short name.

        Parameters:
            name: The analyst name to convert.

        Returns:
            The corresponding short name.
        """
        cls_name = name.split('.')[-1]
        if cls_name != 'Data' and cls_name.endswith('Data'):
            return cls_name[:-4]
        return cls_name

    @staticmethod
    @memoize
    def to_analyst_name(type_: Type) -> str:
        """
        Convert a type to its analyst name.

        Parameters:
            type_: The type to convert.

        Returns:
            The analyst name for the given type.
        """
        type_name = type_.__name__
        module_name = type_.__module__

        # Join module parts, except last, in pascal case
        parts = [to_pascal_case(x) for x in module_name.split('.')[:-1]]
        data_name = f'{".".join(parts)}.{type_.__name__}'

        # Return full analyst name
        if (
            type_name.endswith('Key')
            or type_name.endswith('Query')
            or type_name.endswith('Args')
            or type_name.endswith('Condition')
        ):
            return data_name
        else:
            # Add Data suffix for record types
            return data_name + 'Data'

    @staticmethod
    def get_type_module_to_pascal_case(type_: Type) -> str:
        """
        Get the module name in PascalCase for a type.

        Parameters:
            type_: The type for which to get the module name.

        Returns:
            The module name in PascalCase.
        """
        module_to_pascal_case = '.'.join([to_pascal_case(part) for part in type_.__module__.split('.')[:-1]])

        return module_to_pascal_case

    @staticmethod
    def get_prefixed_name(type_: Type) -> str:
        """Return shortname.type_name if shortname is registered for type. Else returns type_.__name__"""

        type_name = type_.__name__

        # check if shortname is registered for type
        shortname = ClassInfo.get_type_package_shortname(type_)

        if shortname is not None:
            return f'{shortname}.{type_name}'
        else:
            return type_name

    @staticmethod
    def get_type_package_shortname(type_: Type) -> Optional[str]:
        """Return shortname registered by ClassInfo.register_shortname method from Type."""

        return ClassInfo.get_package_shortname(type_.__module__)

    @staticmethod
    def get_module_by_shortname(shortname: str) -> Optional[str]:
        """Return module by shortname if exists."""
        return ClassInfo.__shortname_package_map.get(shortname)

    @staticmethod
    def get_package_shortname(module: str) -> Optional[str]:
        """Return shortname registered by ClassInfo.register_shortname method from module name."""
        for package, shortname in reversed(ClassInfo.__package_shortname_map.items()):
            if module.startswith(package):
                return shortname

    @staticmethod
    def get_type_hints(type_: type) -> Dict[str, type]:
        """
        Return type hints for an object.
        Uses standard typing.get_type_hints with locals param override.
        """

        if not ClassInfo.__is_initialized:
            ClassInfo.__init_types()

        return get_type_hints(type_, localns=ClassInfo.__data_types_map)

    @staticmethod
    @memoize
    def get_ultimate_base(type_: type) -> type:
        """
        Return the ultimate base class of the inheritance chain which determines the collection name.

        This is the class derived directly from Data, Record, or RootRecord.
        """

        from cl.runtime.storage.data_mixin import Data
        from cl.runtime.storage.key_mixin import Key

        type_mro = type_.mro()
        if type_mro[0] in (Data, Key):
            raise Exception('Ultimate base is undefined for Data, Key, ' 'only for classes derived from them.')

        if Key in type_.__bases__:
            raise Exception('Ultimate base is undefined for key classes.')

        for i in range(1, len(type_mro)):
            if type_mro[i] == Key:
                return type_mro[i - 2]
            if type_mro[i] == Data:
                return type_mro[i - 1]
        raise Exception('Type is not derived from Data, Record, or RootRecord.')

    @staticmethod
    def get_collection_name(type_: type) -> str:
        """
        Get the collection name for a type.

        Parameters:
            type_: The type for which to get the collection name.

        Returns:
            The collection name for the given type.
        """
        root_type = ClassInfo.get_ultimate_base(type_)
        return ClassInfo.get_prefixed_name(root_type)

    @staticmethod
    def get_hierarchical_discriminator(type_: type) -> List[str]:
        """Return the inheritance chain of the class as a list of
        class name strings, starting from RootRecord or Record or Data
        and ending with the class itself.

        The class must be derived from Data, error message otherwise.
        """

        from cl.runtime.storage.data_mixin import Data
        from cl.runtime.storage.key_mixin import Key

        type_mro = type_.mro()
        if type_mro[0] in (Data, Key):
            raise Exception('Cannot get inheritance chain for the Root class, ' 'only for classes derived from it.')

        if Key in type_mro:
            idx = type_mro.index(Key)
            if Key in type_.__bases__:
                chain = [ClassInfo.get_prefixed_name(x) for x in type_mro[idx - 1 :: -1]]
            else:
                chain = [ClassInfo.get_prefixed_name(x) for x in type_mro[idx - 2 :: -1]]
            return chain
        elif Data in type_mro:
            idx = type_mro.index(Data)
            return [ClassInfo.get_prefixed_name(x) for x in type_mro[idx - 1 :: -1]]
        raise Exception('Type is not derived from Data')

    @staticmethod
    @memoize
    def get_key_from_record(type_: type) -> type:
        """Extract associated key from Key derived types."""

        from cl.runtime.storage.key_mixin import Key

        type_mro = type_.mro()
        if Key in type_mro:
            data_index = type_mro.index(Key)
            return type_mro[data_index - 1]
        else:
            raise Exception(f'Cannot deduce key from {type_.__name__} type not derived from Key.')

    @staticmethod
    @memoize
    def get_record_from_key(type_: type) -> type:
        """Extract associated record from Key derived types."""

        from cl.runtime.storage.key_mixin import Key

        key_type_name = ClassInfo.get_prefixed_name(type_)

        if Key in type_.mro():
            if not key_type_name.endswith('Key'):
                raise Exception(f'Unexpected type name: {key_type_name}. Key type name should end with "Key"')
            record_type_name = key_type_name[:-3]

            # Load by record name
            record_type = ClassInfo.get_type(record_type_name)
            return record_type
        else:
            raise Exception(f'Cannot deduce record from {type_.__name__} type not derived from Key.')

    @staticmethod
    def __init_types():
        """Initialize types, resolving issues with class duplicates in __subclasses__()."""
        from cl.runtime.storage.context import Context
        from cl.runtime.storage.data_mixin import Data

        # Resolves issue with classes duplicates in __subclasses__()
        gc.collect()
        children = ClassInfo.__get_runtime_imported_data(Data, [Context, Data])
        for child in children:
            an_name = ClassInfo.to_analyst_name(child)
            prefixed_name = ClassInfo.get_prefixed_name(child)
            existed_child = ClassInfo.__data_types_map.get(prefixed_name, None)

            # TODO: investigate type collisions
            # Add only new child types except runtime duplicate classes
            # if existed_child is None or existed_child.__module__.startswith('cl.runtime.schema.declaration'):
            if existed_child is None:
                ClassInfo.__data_types_map[child.__name__] = child
                ClassInfo.__data_types_map[prefixed_name] = child
                ClassInfo.__data_types_map[an_name] = child

        ClassInfo.__is_initialized = True

    @staticmethod
    def __get_runtime_imported_data(type_: type, children: List[type]) -> List[type]:
        """For the given type recursively add its children."""
        current_children = type_.__subclasses__()
        for t in current_children:
            ClassInfo.__get_runtime_imported_data(t, children)
        children.extend(current_children)
        return children

    @staticmethod
    def get_class_fields(
        data_type: type,
        *,
        as_dict: bool = False,
        recurse: bool = True,
        as_attributes: bool = False,
        serializable: bool = False,
    ) -> Union[List[Any], Dict[str, Any]]:
        """Return class fields in dict notation or as list.

        Args:
            data_type: type of given input
            as_dict: returns fields in dict notation
            recurse: marks recurse flag, acceptable for 'attrs' transformed types, otherwise ignored
            as_attributes: marks return value type, acceptable for 'dataclass' transform and as_dict=True,
        otherwise ignored, returns result as {'field_name': Field(...)} if True
            serializable: returns only serializable fields (excludes protected and context)
        """
        class_fields = None
        if transform_attr := getattr(data_type, Transform.dataclass.value, None):
            class_fields = list(transform_attr.values())
            if as_dict:
                if as_attributes:
                    class_fields = transform_attr
                else:
                    class_keys = transform_attr.keys()
                    class_fields = {class_key: getattr(data_type, class_key) for class_key in class_keys}

        elif transform_attr := getattr(data_type, Transform.attrs.value, None):
            class_fields = transform_attr
            if as_dict:
                if isinstance(data_type, ABCMeta):
                    fields = getattr(data_type, Transform.attrs.value, [])
                    class_fields = {f.name: f for f in fields} if fields else None
                else:
                    class_fields = attrs.asdict(data_type, recurse=recurse)
        if not class_fields:
            raise ValueError(f'Type {data_type} is not correctly decorated')

        if serializable:
            serializable_fields = [field.name for field in ClassInfo.get_serializable_fields(data_type)]
            if isinstance(class_fields, dict):
                class_fields_ = {}
                for key, value in class_fields.items():
                    if key in serializable_fields:
                        class_fields_[key] = value
                return class_fields_
            else:
                class_fields = [field for field in class_fields if field not in serializable_fields]

        return class_fields

    @staticmethod
    def get_serializable_fields(data_type: type, remove_protected: bool = True) -> List[Any]:
        """Get serializable fields of the given data type.

        Args:
            data_type (type): The type of the input data.
            remove_protected (bool, optional): Whether to exclude protected fields (those starting with '_').
                Defaults to True.

        Returns:
            List[Any]: List of serializable fields.

        Raises:
            ValueError: If the provided data type is not correctly decorated.

        Note:
            This function identifies serializable fields by comparing them with the fields defined in the base
            `cl.runtime.storage.data.Data` class. It excludes fields starting with '_' if `remove_protected` is True.
        """
        from cl.runtime.storage.data_mixin import Data

        data_fields = vars(Data).keys()
        class_fields = ClassInfo.get_class_fields(data_type)
        fields_ = []
        for field_ in class_fields:
            if field_.name not in data_fields:
                if remove_protected:
                    if not field_.name.startswith('_'):
                        fields_.append(field_)
                else:
                    fields_.append(field_)
        return fields_

    @staticmethod
    def get_transform(data_type: type) -> Optional[str]:
        """Return transform if class is decorated.

        Args:
            data_type: type of given input
        """

        return (
            getattr(data_type, Transform.dataclass.value, None)
            or getattr(data_type, Transform.attrs.value, None)
            or None
        )

    @staticmethod
    def __remove_shortname_related_types(module_name: str, shortname: str) -> None:
        """
        Remove entries from ClassInfo's data types map with keys starting with the provided shortname based on the
        provided module_name.

        Parameters:
        - module_name (str): The module name used to identify keys in the data_types_map for removal,
          represented in dot-separated format (e.g., 'my.module').
        - shortname (str): The shortname used to identify keys in the data_types_map for removal.

        Usage:
        This method will remove entries in data_types_map where the key corresponding to the provided
        shortname, e.g. starts with 'custom' and its module_name, e.g.  value can be accessible by
        the key which starts with 'module_name' in PascalCase.
        """
        module_name_in_pascal_case = ClassInfo.__module_name_to_pascal_case(module_name)

        # Find keys in __data_types_map that start with the given module_name in pascal case and its values respectively
        shortname_related_keys = [
            key for key in ClassInfo.__data_types_map if key.startswith(module_name_in_pascal_case)
        ]
        shortname_related_values = [ClassInfo.__data_types_map[key] for key in shortname_related_keys]
        # Find keys in __data_types_map that start with the given shortname
        keys_to_remove = [key for key in ClassInfo.__data_types_map if key.startswith(shortname)]

        for key in keys_to_remove:
            temp_value = ClassInfo.__data_types_map[key]
            if temp_value in shortname_related_values:
                del ClassInfo.__data_types_map[key]

    @staticmethod
    def __add_shortname_related_types(module_name: str, shortname: str) -> None:
        """
        Add new entries to the ClassInfo.__data_types_map dictionary based on the given shortname.

        Parameters:
            module_name (str): The name of the module in dot-separated format (e.g., 'my.module').
            shortname (str): The shortname to be used for creating new keys in __data_types_map.

        Usage:
        If module_name = 'my.module' and shortname = 'custom', new values where keys in __data_types_map starting
        with 'My.Module' will be added, however, keys for new values will be started with 'custom' instead.
        """
        module_name_in_pascal_case = ClassInfo.__module_name_to_pascal_case(module_name)

        # Find keys in __data_types_map that start with the given module_name
        keys_to_update = [key for key in ClassInfo.__data_types_map if key.startswith(module_name_in_pascal_case)]

        for key in keys_to_update:
            new_key = f'{shortname}.{ClassInfo.__data_types_map[key].__name__}'
            ClassInfo.__data_types_map[new_key] = ClassInfo.__data_types_map[key]

    @staticmethod
    def __module_name_to_pascal_case(module_name: str) -> str:
        """
        Convert a module name to PascalCase.

        This function takes a module name in dot-separated form (e.g., 'example.module.name')
        and converts it to PascalCase (e.g., 'Example.Module.Name').

        Parameters:
            module_name (str): The module name to be converted.

        Returns:
            str: The module name in PascalCase.

        Example:
        If module_name = 'example.module.name', the returned value will be 'Example.Module.Name'.
        """
        parts = [to_pascal_case(x) for x in module_name.split('.')]
        module_name_in_pascal_case = '.'.join(parts)
        return module_name_in_pascal_case
