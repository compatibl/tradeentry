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

import pytest
import json
import os
import inspect
import ast
import dataclasses
from typing import Any, List, Dict, Type

from inflection import titleize

from cl.runtime.schema.type_decl import TypeDecl
from stubs.cl.runtime import StubDataclassRecord, StubDataclassNestedFields

sample_types = [
    StubDataclassRecord,
    StubDataclassNestedFields
]


def get_field_names(cls, method_name):
    """Get key field names from get_key method, assuming it follows the standard implementation pattern."""

    # Parse the class to get its AST node
    class_ast = ast.parse(inspect.getsource(cls))

    # Find the method within the class
    method_ast = None
    for node in class_ast.body:
        if isinstance(node, ast.ClassDef) and node.name == cls.__name__:
            for method in node.body:
                if isinstance(method, ast.FunctionDef) and method.name == method_name:
                    method_ast = method
                    break

    if method_ast is None:
        return []

    # Extract field names from the method AST
    field_names = []
    for node in ast.walk(method_ast):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == 'self':
            field_names.append(node.attr)

    return field_names


def get_type_decl(cls: Type) -> Dict[str, Any]:
    """Get type declaration for a class."""

    elements = []

    for field in dataclasses.fields(cls):
        element = {
            "value": {
                "type": field.type.__name__
            },
            "name": field.name,
            "comment": field.metadata.get("comment", "")
        }
        elements.append(element)

    type_decl = {
        "module": {
            "module_name": cls.__module__
        },
        "name": cls.__name__,
        "label": titleize(cls.__name__),
        "comment": cls.__doc__ or "",
        "display_kind": "Basic",
        "elements": elements,
        "keys": get_field_names(cls, 'get_key'),
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
        assert result_obj == expected_result_obj


if __name__ == "__main__":
    pytest.main([__file__])
