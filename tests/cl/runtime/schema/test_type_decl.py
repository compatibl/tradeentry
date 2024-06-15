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
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.schema.type_decl import TypeDecl

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
            StringUtil.to_snake_case(key) if isinstance(key, str) else key: to_snake_case(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [to_snake_case(item) for item in data]
    else:
        return data


def test_init():
    """Test TypeDecl __init__ method."""

    type_decl_dict_snake_case = to_snake_case(type_decl_dict)
    result = TypeDecl(**type_decl_dict_snake_case)

    assert result.name == type_decl_dict["Name"]

    module_name_from_dict = type_decl_dict["Module"]["ModuleName"]
    module_name_from_obj = result.module["module_name"]  # TODO: Currently maps to dictionary rather than tuple
    assert module_name_from_obj == module_name_from_dict

    key, (record_type, record_dict) = result.pack()
    assert record_dict == type_decl_dict_snake_case


if __name__ == "__main__":
    pytest.main([__file__])
