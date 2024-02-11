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

from copy import copy
from typing import Any, Dict, Generic, List, Optional, Type, get_args, get_origin

from typing_inspect import get_generic_bases

from cl.runtime.primitive.schema_helper import element_name_to_schema
from cl.runtime.serialization.type_info import TypeInfo, TypeKind, get_type_methods, set_generic_params
from cl.runtime.storage.class_info import ClassInfo
from cl.runtime.storage.attrs import data_field


class RecordFieldInfo:
    """Holds record field info."""

    field: Optional[Any] = data_field()
    """Field as object."""

    declared_type: Optional[Type] = data_field()
    """Field declared type."""

    type_info: Optional[TypeInfo] = data_field()
    """Field declared type info."""

    name: Optional[str] = data_field()
    """Field name."""

    schema_name: Optional[str] = data_field()
    """Field schema name."""

    def __init__(self, field: Any, field_type: type):
        """Initialize a RecordFieldInfo instance.

        Args:
            field (Any): The field as an object.
            field_type (type): The field declared type.
        """
        self.field = field
        self.declared_type = field_type
        self.type_info = TypeInfo(field_type, field.metadata)

        self.name: str = field.name
        self.schema_name: str = element_name_to_schema(field)


# TODO(attrs) - move __types_map to another class to avoid using auto_attribs=False
class RecordInfo:
    """Holds info for record type."""

    __types_map: Dict[type, 'RecordInfo'] = dict()
    """Container to hold already created RecordInfo objects. Used as cache."""

    fields: Optional[List[RecordFieldInfo]] = data_field()
    """List of fields info."""

    methods: Optional[Dict[str, 'MethodInfo']] = data_field()  # noqa
    """List of methods info."""

    def __init__(self, data_type: type):
        """Extract record type information."""

        self.fields: List[RecordFieldInfo] = list()

        serializable_fields = ClassInfo.get_serializable_fields(data_type)

        hints = ClassInfo.get_type_hints(data_type)

        # iterate type fields
        for field in serializable_fields:
            field_type = RecordFieldInfo(field, hints[field.name])
            self.fields.append(field_type)

        type_methods = get_type_methods(data_type)
        from cl.runtime.serialization.method_info import MethodInfo

        self.methods = {method_name: MethodInfo(data_type, method_name) for method_name in type_methods}

    def get_generic_type_hints(self, expected_type: TypeInfo) -> List[RecordFieldInfo]:
        """Replace generic fields type with generic argument."""

        if not expected_type.is_generic:
            return self.fields

        generic_base = next(x for x in get_generic_bases(expected_type.real_type) if get_origin(x) == Generic)
        generic_args = get_args(generic_base)
        type_args = get_args(expected_type.type)
        type_args_map = dict(zip(generic_args, type_args))

        # Update fields info with filled generic args
        typed_fields: List[RecordFieldInfo] = list()

        for field in self.fields:
            field_type_info = field.type_info

            if field_type_info.is_generic or field_type_info.kind == TypeKind.GenericArgument:
                typed_field = copy(field)
                filled_type = set_generic_params(field.declared_type, type_args_map)
                typed_field.type_info = TypeInfo(filled_type, field.field.metadata)
            else:
                typed_field = field

            typed_fields.append(typed_field)

        return typed_fields

    @classmethod
    def get_type_info(cls, type_: type) -> 'RecordInfo':
        """Get type info from cache or create new RecordInfo object."""
        type_info = cls.__types_map.get(type_, None)

        if type_info is None:
            type_info = RecordInfo(type_)
            cls.__types_map[type_] = type_info

        return type_info

    @classmethod
    def get_method_info(cls, type_: type, method_name: str) -> 'MethodInfo':  # noqa
        """Get method info from cache or create new Method info object."""
        type_info = cls.get_type_info(type_)
        method_info = type_info.methods.get(method_name, None)

        if method_info is None:
            raise ValueError(f'Type {type_} has no method {method_name}.')

        return method_info
