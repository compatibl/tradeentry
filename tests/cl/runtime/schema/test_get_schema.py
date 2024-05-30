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

import pytest
import json
import os
import inspect
import textwrap
import ast
import dataclasses
from dataclasses import dataclass, Field
from typing import Tuple, Type, Any, List, Dict, get_type_hints

from inflection import titleize

from cl.runtime.schema.type_decl import TypeDecl
from stubs.cl.runtime import StubDataclassRecord, StubDataclassNestedFields
from stubs.cl.runtime.records.dataclasses.stub_dataclass_optional_fields import StubDataclassOptionalFields


@dataclass(slots=True, init=False)
class DataclassFieldType:
    """Field type of a dataclass."""

    def __init__(self, field: Field):
        """Create from dataclasses.Field instance."""

        field_type = field.type
        field_origin = typing.get_origin(field_type)
        field_args = typing.get_args(field_type)

        # Strip optional from field_type
        # Note two possible forms of origin for optional, typing.Union and types.UnionType
        if (field_origin is typing.Union or field_origin is types.UnionType) and type(None) in field_args:
            # This is an optional field
            self.optional_field = True
            # Get type information without None
            field_type = field_args[0]
            field_origin = typing.get_origin(field_type)
            field_args = typing.get_args(field_type)
        else:
            # This is a required field
            self.optional_field = False

        # Set container type or None if not a container
        self.container_type = typing.get_origin(field_type)

        # Validate that container type is one of the supported types
        if self.container_type not in [None, tuple, list, dict]:
            raise RuntimeError(f"Container type {self.container_type} is not a supported part of schema.")

        if self.container_type is not None:
            # Strip container information from field_type
            self.value_type = typing.get_args(field_type)[0]
            list_type_origin = typing.get_origin(self.value_type)
            if (list_type_origin is typing.Union or list_type_origin is types.UnionType) and type(None) in typing.get_args(self.value_type):
                # Values within the container can be None
                self.optional_values = True
                # Get type information without None
                self.value_type = typing.get_args(self.value_type)[0]
            else:
                # Values within the container cannot be None
                self.optional_values = False
        else:
            self.value_type = field_type
            self.optional_values = False

    value_type: Type
    """Type of the value within the container if the field is a container, otherwise type of the field itself."""

    container_type: Type | None
    """Type of the container (list, dict, etc.) if the field is a container, otherwise None."""

    optional_field: bool
    """Indicates if the entire field can be None."""

    optional_values: bool | None
    """Indicates if values within the container can be None if the field is a container, otherwise None."""



sample_types = [
    # StubDataclassRecord,
    StubDataclassOptionalFields,
    StubDataclassNestedFields
]


def get_key_fields(cls):  # TODO: Move to a dedicated helper class
    """
    Get key fields by parsing the source of 'get_key' method.

    Notes:
        This method parses the source code of 'get_key' method and returns all instance
        fields it accesses in the order of access, for example if 'get_key' source is:

        def get_key(self) -> Tuple[Type, ...]:
            return ClassName, self.key_field_1, self.key_field_2

        this method will return:

        ["key_field_1", "key_field_2"]
    """

    # Get source code for the 'get_key' method
    if hasattr(cls, 'get_key'):
        get_key_source = inspect.getsource(cls.get_key)
    else:
        raise RuntimeError(f"Cannot get primary key fields because {cls.__name__} does not implement 'get_key' method.")

    # Because 'ast' expects the code to be correct as though it is at top level,
    # remove excess indent from the source to make it suitable for parsing
    get_key_source = textwrap.dedent(get_key_source)

    # Extract field names from the AST of 'get_key' method
    get_key_ast = ast.parse(get_key_source)
    key_fields = []
    for node in ast.walk(get_key_ast):
        # Find every instance field of 'cls' accessed inside the source of 'get_key' method.
        # Accumulate in list in the order they are accessed
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == 'self':
            key_fields.append(node.attr)

    return key_fields


def get_type_decl(cls: Type) -> Dict[str, Any]:
    """Get type declaration for a class."""

    elements = []
    fields = dataclasses.fields(cls)
    for field in fields:
        field_type = DataclassFieldType(field)
        print(f'{field.name}:{field_type}')

        #element = {
        #    "value": {
        #        "type": field.type.__name__
        #    },
        #    "name": field.name,
        #    "comment": field.metadata.get("comment", "")
        #}
        #elements.append(element)

    # Get key fields by parsing the source of 'get_key' method
    key_fields = get_key_fields(cls)

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
