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

import json
import os
import pytest

from cl.runtime.schema.dataclasses.dataclass_type_decl import DataclassTypeDecl
from cl.runtime.schema.type_decl import TypeDecl
from inflection import titleize
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.records.dataclasses.stub_dataclass_optional_fields import StubDataclassOptionalFields
from typing import Any
from typing import Dict
from typing import Type


def get_type_decl(cls: Type) -> Dict[str, Any]:
    """Get type declaration for a class."""

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

        expected_result_obj = DataclassTypeDecl(**expected_result)
        result_obj = DataclassTypeDecl.for_type(sample_type)
        pass
        # TODO: Compare assert result_obj == expected_result_obj


if __name__ == "__main__":
    pytest.main([__file__])
