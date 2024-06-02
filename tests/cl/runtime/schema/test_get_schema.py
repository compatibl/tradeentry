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

import types
import typing
from enum import Enum
import pytest
import json
import os
import dataclasses
import datetime as dt
from dataclasses import dataclass, Field
from typing import Tuple, Literal, Type, Any, List, Dict, get_type_hints
from inflection import titleize
from cl.runtime.records.schema_util import SchemaUtil
from cl.runtime.schema.type_decl import TypeDecl
from stubs.cl.runtime import StubDataclassRecord, StubDataclassNestedFields
from stubs.cl.runtime.records.dataclasses.stub_dataclass_optional_fields import StubDataclassOptionalFields


@dataclass(slots=True, init=False)
class DataclassFieldType:
    """Field type of a dataclass."""

    def __init__(self, field: Field, field_type: Type):
        """
        Create from dataclasses.Field instance and resolved type.

        Notes:
            The Field object also contains the type but if it is a ForwardRef, it will not be resolved.

        Args:
            field: Dataclass field definition object
            field_type: Field type obtained from get_type_hints where ForwardRefs are resolved
        """

        field_name = field.name
        field_origin = typing.get_origin(field_type)
        field_args = typing.get_args(field_type)

        # Note two possible forms of origin for optional, typing.Union and types.UnionType
        is_union = field_origin is typing.Union or field_origin is types.UnionType
        is_optional = is_union and type(None) in field_args

        # Strip optional from field_type
        if is_optional:
            # Field can be None
            self.optional_field = True
            # Get type information without None
            field_type = field_args[0]
            field_origin = typing.get_origin(field_type)
            field_args = typing.get_args(field_type)
        else:
            # Field cannot be None
            self.optional_field = False

        # Strip container information from field_type to get the type of value inside the container
        if field_origin in [list, dict]:
            # One of the supported container types
            self.container_type = field_origin
            field_type = field_args[0]
            field_origin = typing.get_origin(field_type)
            field_args = typing.get_args(field_type)
        else:
            # No container
            self.container_type = None

        # Strip optional again from the inner type
        is_union = field_origin is typing.Union or field_origin is types.UnionType
        is_optional = is_union and type(None) in field_args
        if is_optional:
            # Values can be None
            self.optional_values = True
            # Get type information without None
            field_type = field_args[0]
            field_origin = typing.get_origin(field_type)
            field_args = typing.get_args(field_type)
        else:
            # Values cannot be None
            self.optional_values = False

        # Parse the value itself
        if field_origin is tuple:

            # Key is represented as a tuple
            self.element_kind = "key"

            # Get the first argument of Tuple
            tuple_args = typing.get_args(field_type)
            if len(tuple_args) == 0:
                raise RuntimeError(f"Empty tuple is provided as value for field {field_name}")
            tuple_arg = tuple_args[0]

            type_origin = typing.get_origin(tuple_arg)
            if isinstance(type_origin, type):
                # Extract SampleType from Type[SampleType] or Type['SampleType']
                type_args = typing.get_args(tuple_arg)
                if len(type_args) == 0:
                    raise RuntimeError(f"Type without arguments is provided as value for key field {field_name}, "
                                       f"use Type[SampleType] or Type['SampleType'] instead.")

                # Get the argument of Type
                type_arg = type_args[0]
                if isinstance(type_arg, typing.ForwardRef):
                    # For ForwardRef, extract the argument
                    type_arg = type_arg.__forward_arg__

            else:
                raise RuntimeError(f"First element of key tuple for field {field_name} is not a type.")

            # Assign key type
            self.element_type = type_arg

        elif field_origin is None:

            # Assign element kind
            if field_type in [str, float, bool, int, dt.date, dt.time, dt.datetime]:
                # One of the supported primitive types
                self.element_kind = "primitive"
            elif issubclass(field_type, Enum):
                # Enum
                self.element_kind = "enum"
            else:
                # User-defined data or record
                self.element_kind = "data"

            # Assign element type
            self.element_type = field_type

        else:
            raise RuntimeError(f"Complex type {field_type} is not recognized when building data source schema.")

    element_kind: Literal["primitive", "key", "data", "enum"]
    """Kind of the element within the container if the field is a container, otherwise kind of the field itself."""

    element_type: Type
    """Type of the element within the container if the field is a container, otherwise type of the field itself."""

    container_type: Type | None
    """Type of the container (list, dict, etc.) if the field is a container, otherwise None."""

    optional_field: bool
    """Indicates if the entire field can be None."""

    optional_values: bool | None = None
    """Indicates if values within the container can be None if the field is a container, otherwise None."""


def get_type_decl(cls: Type) -> Dict[str, Any]:
    """Get type declaration for a class."""

    # Information about dataclass fields including the metadata (does not resolve ForwardRefs)
    fields = dataclasses.fields(cls)

    # Get type hints to resolve ForwardRefs
    type_hints = get_type_hints(cls)

    elements = []
    for field in fields:

        field_type = type_hints[field.name]
        field_decl = DataclassFieldType(field, field_type)
        pass

        #element = {
        #    "value": {
        #        "type": field.type.__name__
        #    },
        #    "name": field.name,
        #    "comment": field.metadata.get("comment", "")
        #}
        #elements.append(element)

    # Get key fields by parsing the source of 'get_key' method
    key_fields = SchemaUtil.get_key_fields(cls)

    type_decl = {
        "module": {
            "module_name": cls.__module__
        },
        "name": cls.__name__,
        "label": titleize(cls.__name__),
        "comment": cls.__doc__ or "",
        "kind": "Element",
        "display_kind": "Basic",
        "elements": elements,
        "keys": key_fields,
        "implement": {
            "handlers": []
        }
    }

    return type_decl


def test_method():
    """Test coroutine for /schema/typeV2 route."""

    sample_types = [
        StubDataclassRecord,
        StubDataclassOptionalFields,
        StubDataclassNestedFields
    ]

    for sample_type in sample_types:
        class_module = sample_type.__module__.rsplit(".", maxsplit=1)[1]
        expected_result_file_path = os.path.abspath(__file__).replace(".py", f".{class_module}.expected.json")
        with open(expected_result_file_path, 'r', encoding='utf-8') as file:
            expected_result = json.load(file)

        expected_result_obj = TypeDecl(**expected_result)
        result_dict = get_type_decl(sample_type)
        result_obj = TypeDecl(**result_dict)
        # assert result_obj == expected_result_obj TODO: Restore


if __name__ == "__main__":
    pytest.main([__file__])
