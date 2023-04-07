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
from functools import cache
from typing import Dict, List, Set, Type, TypeVar, get_type_hints


from cl.runtime.core.primitive.string_util import to_pascal_case
from cl.runtime.core.storage.class_record import ClassRecord

T = TypeVar('T')


class TypeUtil:
    """Contains reflection based helper static methods."""

    __is_initialized: bool = False
    __data_types_map: Dict[str, type] = dict()
    __package_shortname_map: Dict[str, str] = dict()

    @staticmethod
    def register_shortname(module_name: str, shortname: str):
        TypeUtil.__package_shortname_map[module_name] = shortname

    @staticmethod
    def unregister_shortname(module_name: str):
        TypeUtil.__package_shortname_map.pop(module_name)

    @staticmethod
    @cache
    def get_derived_types(module_name: str, base_type: Type[T]) -> Set[Type[T]]:
        """Extract all derived classes from specified module."""
        try:
            module_ = importlib.import_module(module_name)
        except ImportError as error:
            raise RuntimeError(f'Cannot import module: {error.name}. Check sys.path')

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
        """Returns data derived type given its name."""

        if not TypeUtil.__is_initialized or name not in TypeUtil.__data_types_map:
            # Try to update map one more time. This scenario is possible depending on
            # first call to get_type and which classes where imported at that moment.
            TypeUtil.__init_types()

            if name not in TypeUtil.__data_types_map:
                raise RuntimeError(
                    f'Class {name} is not found in TypeUtil data types map. ' f'Import this class before loading.'
                )

        return TypeUtil.__data_types_map[name]

    @staticmethod
    def try_get_type(name: str) -> type:
        """Returns data derived type given its name. Returns None if not found"""

        if not TypeUtil.__is_initialized:
            TypeUtil.__init_types()

        return TypeUtil.__data_types_map.get(name, None)

    @staticmethod
    @cache
    def from_analyst_to_short_name(name: str) -> str:
        cls_name = name.split('.')[-1]
        if cls_name != 'ClassData' and cls_name.endswith('Data'):
            return cls_name[:-4]
        return cls_name

    @staticmethod
    @cache
    def to_analyst_name(type_: Type) -> str:
        type_name = type_.__name__
        module_name = type_.__module__

        # cl.finance -> cl.analyst.finance
        if module_name.startswith('cl.finance'):
            module_name = 'cl.analyst.' + module_name[3:]

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
    def get_prefixed_name(type_: Type) -> str:
        type_module = type_.__module__
        type_name = type_.__name__

        for package, shortname in TypeUtil.__package_shortname_map.items():
            if type_module.startswith(package):
                return f'{shortname}.{type_name}'

        return type_name

    @staticmethod
    def get_type_hints(type_: type) -> Dict[str, type]:
        """
        Return type hints for an object.
        Uses standard typing.get_type_hints with locals param override.
        """

        if not TypeUtil.__is_initialized:
            TypeUtil.__init_types()

        return get_type_hints(type_, localns=TypeUtil.__data_types_map)

    @staticmethod
    @cache
    def get_ultimate_base(type_: type) -> type:
        """
        Returns the ultimate base class of the inheritance chain which
        determines the collection name.

        This is the class derived directly from Data, Record, or RootRecord.
        """

        from cl.runtime.core.storage.class_data import ClassData
        from cl.runtime.core.storage.class_record import ClassRecord

        type_mro = type_.mro()
        if type_mro[0] in (ClassData, ClassRecord):
            raise RuntimeError('Ultimate base called for the abstract base itself.')

        if ClassRecord in type_.__bases__:
            raise RuntimeError('Ultimate base is undefined for a key class.')

        for i in range(1, len(type_mro)):
            if type_mro[i] == ClassRecord:
                return type_mro[i - 2]
            if type_mro[i] == ClassData:
                return type_mro[i - 1]
        raise RuntimeError('Type is not derived from ClassData or ClassRecord.')

    @staticmethod
    def get_collection_name(type_: type) -> str:
        root_type = TypeUtil.get_ultimate_base(type_)
        return TypeUtil.get_prefixed_name(root_type)

    @staticmethod
    def get_hierarchical_discriminator(type_: type) -> List[str]:
        """Returns the inheritance chain of the class as a list of
        class name strings, starting from RootRecord or Record or Data
        and ending with the class itself.

        The class must be derived from Data, error message otherwise.
        """

        from cl.runtime.core.storage.class_data import ClassData
        from cl.runtime.core.storage.class_record import ClassRecord
        from cl.runtime.core.storage.deleted_record import DeletedRecord

        type_mro = type_.mro()
        if type_mro[0] in (ClassData, ClassRecord):
            raise RuntimeError('Cannot get inheritance chain for the Root class, only for classes derived from it.')

        if ClassRecord in type_mro:
            idx = type_mro.index(ClassRecord)
            if idx == 0:
                raise RuntimeError("ClassRecord is an abstract base that should not be used directly.")
            if ClassRecord in type_.__bases__:
                chain = [TypeUtil.get_prefixed_name(x) for x in type_mro[idx - 1::-1]]
            else:
                chain = [TypeUtil.get_prefixed_name(x) for x in type_mro[idx - 2::-1]]
            return chain
        elif ClassData in type_mro:
            idx = type_mro.index(ClassData)
            if idx == 0:
                raise RuntimeError("ClassData is an abstract base that should not be used directly.")
            return [TypeUtil.get_prefixed_name(x) for x in type_mro[idx - 1::-1]]
        elif DeletedRecord in type_mro:
            idx = type_mro.index(DeletedRecord)
            if idx != 0:
                raise RuntimeError("DeletedRecord is a final class that should not be derived from.")
            return [TypeUtil.get_prefixed_name(type_mro[0])]
        raise RuntimeError('Type is not derived from ClassData')

    @staticmethod
    @cache
    def get_key_from_record(type_: type) -> type:
        """Extracts associated key from ClassRecord derived types."""

        from cl.runtime.core.storage.class_record import ClassRecord

        type_mro = type_.mro()
        if ClassRecord in type_mro:
            data_index = type_mro.index(ClassRecord)
            return type_mro[data_index - 1]
        else:
            raise RuntimeError(f'Cannot deduce key from {type_.__name__} type not derived from ClassRecord.')

    @staticmethod
    @cache
    def get_record_from_key(type_: type) -> type:
        """Extracts associated record from ClassRecord derived types."""

        from cl.runtime.core.storage.class_record import ClassRecord

        key_type_name = TypeUtil.get_prefixed_name(type_)

        if ClassRecord in type_.mro():
            if not key_type_name.endswith('Key'):
                raise RuntimeError(f'Unexpected type name: {key_type_name}. Key type name should end with "Key"')
            record_type_name = key_type_name[:-3]

            # Load by record name
            record_type = TypeUtil.get_type(record_type_name)
            return record_type
        else:
            raise RuntimeError(f'Cannot deduce record from {type_.__name__} type not derived from ClassRecord.')

    @staticmethod
    def __init_types():
        from cl.runtime.core.storage.context import Context
        from cl.runtime.core.storage.class_data import ClassData

        # Resolves issue with classes duplicates in __subclasses__()
        gc.collect()
        children = TypeUtil.__get_runtime_imported_data(ClassData, [Context, ClassData])
        children.extend(TypeUtil.__get_runtime_imported_data(ClassRecord, [ClassRecord]))
        for child in children:
            an_name = TypeUtil.to_analyst_name(child)
            prefixed_name = TypeUtil.get_prefixed_name(child)
            existed_child = TypeUtil.__data_types_map.get(prefixed_name, None)

            # TODO: investigate type collisions
            # Add only new child types except runtime duplicate classes
            # if existed_child is None or existed_child.__module__.startswith('cl.runtime.core.schema.declaration'):
            if existed_child is None:
                TypeUtil.__data_types_map[child.__name__] = child
                TypeUtil.__data_types_map[prefixed_name] = child
                TypeUtil.__data_types_map[an_name] = child

        TypeUtil.__is_initialized = True

    @staticmethod
    def __get_runtime_imported_data(type_: type, children: List[type]) -> List[type]:
        """For the given type recursively adds its children."""
        current_children = type_.__subclasses__()
        for t in current_children:
            TypeUtil.__get_runtime_imported_data(t, children)
        children.extend(current_children)
        return children
