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
from typing import Any, List, Dict, Type, get_type_hints

from inflection import titleize

from cl.runtime.schema.type_decl import TypeDecl
from stubs.cl.runtime import StubDataclassRecord, StubDataclassNestedFields
from stubs.cl.runtime.records.dataclasses.stub_dataclass_optional_fields import StubDataclassOptionalFields

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


def parse_field_type(field_type):
    origin = typing.get_origin(field_type)
    args = typing.get_args(field_type)

    if (origin is typing.Union or origin is types.UnionType) and type(None) in args:
        # This is an Optional type
        actual_type = args[0]  # Get the type without None
        category = 'Optional'
    else:
        actual_type = field_type
        category = 'Required'

    if typing.get_origin(actual_type) is list:
        # This is a list
        list_type = typing.get_args(actual_type)[0]
        list_type_origin = typing.get_origin(list_type)
        if (list_type_origin is typing.Union or list_type_origin is types.UnionType) and type(None) in typing.get_args(list_type):
            # List of Optionals
            list_elem_type = typing.get_args(list_type)[0]
            list_category = 'List of Optional'
        else:
            # List of Required
            list_elem_type = list_type
            list_category = 'List of Required'
        return f'{category} {list_category} {list_elem_type}'
    else:
        return f'{category} {actual_type}'

def get_type_decl(cls: Type) -> Dict[str, Any]:
    """Get type declaration for a class."""

    elements = []
    fields = dataclasses.fields(cls)
    for field in fields:
        field_type = field.type
        description = parse_field_type(field_type)
        print(f'{field.name}: {description}')

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
