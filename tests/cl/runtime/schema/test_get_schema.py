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

import dataclasses
import datetime as dt
import json
import os
import pytest
import types
import typing
from cl.runtime.records.schema_util import SchemaUtil
from cl.runtime.schema.dataclasses.dataclass_field_decl import DataclassFieldDecl
from cl.runtime.schema.type_decl import TypeDecl
from dataclasses import Field
from dataclasses import dataclass
from enum import Enum
from inflection import titleize
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.records.dataclasses.stub_dataclass_optional_fields import StubDataclassOptionalFields
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Tuple
from typing import Type
from typing import get_type_hints


def get_type_decl(cls: Type) -> Dict[str, Any]:
    """Get type declaration for a class."""

    # Information about dataclass fields including the metadata (does not resolve ForwardRefs)
    fields = dataclasses.fields(cls)

    # Get type hints to resolve ForwardRefs
    type_hints = get_type_hints(cls)

    elements = []
    for field in fields:
        field_type = type_hints[field.name]
        field_decl = DataclassFieldDecl.create(field, field_type)
        pass

        # element = {
        #    "value": {
        #        "type": field.type.__name__
        #    },
        #    "name": field.name,
        #    "comment": field.metadata.get("comment", "")
        # }
        # elements.append(element)

    # Get key fields by parsing the source of 'get_key' method
    key_fields = SchemaUtil.get_key_fields(cls)

    type_decl = {
        "module": {"module_name": cls.__module__},
        "name": cls.__name__,
        "label": titleize(cls.__name__),
        "comment": cls.__doc__ or "",
        "kind": "Element",
        "display_kind": "Basic",
        "elements": elements,
        "keys": key_fields,
    }

    return type_decl


def test_method():
    """Test coroutine for /schema/typeV2 route."""

    sample_types = [StubDataclassRecord, StubDataclassOptionalFields, StubDataclassNestedFields]

    for sample_type in sample_types:
        class_module = sample_type.__module__.rsplit(".", maxsplit=1)[1]
        expected_result_file_path = os.path.abspath(__file__).replace(".py", f".{class_module}.expected.json")
        with open(expected_result_file_path, "r", encoding="utf-8") as file:
            expected_result = json.load(file)

        expected_result_obj = TypeDecl(**expected_result)
        result_dict = get_type_decl(sample_type)
        result_obj = TypeDecl(**result_dict)
        # assert result_obj == expected_result_obj TODO: Restore


if __name__ == "__main__":
    pytest.main([__file__])
