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
from cl.runtime.backend.core.ui_app_state import UiAppState
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.schema.type_decl import TypeDecl
from stubs.cl.runtime import StubDataclassRecord

type_decl_dict = {
    "Module": {"ModuleName": "Cl.Runtime.Backend.Core"},
    "Name": "UiAppState",
    "DisplayKind": "Basic",
    "Elements": [
        {"Value": {"Type": "String"}, "Name": "User", "Optional": True},
    ],
    "Keys": ["User"],
}


def to_snake_case(data):
    if isinstance(data, dict):
        return {
            StringUtil.pascal_to_snake_case(key) if isinstance(key, str) else key: to_snake_case(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [to_snake_case(item) for item in data]
    else:
        return data


def test_to_type_decl_dict():
    """Test TypeDecl.to_type_decl_dict method."""

    record_types = [UiAppState, StubDataclassRecord]

    for record_type in record_types:
        type_decl = TypeDecl.for_type(UiAppState)
        type_decl_dict = type_decl.to_type_decl_dict()
        pass


if __name__ == "__main__":
    pytest.main([__file__])
