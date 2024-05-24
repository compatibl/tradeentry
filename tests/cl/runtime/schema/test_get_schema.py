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
from cl.runtime.schema.type_decl import TypeDecl

module_names = [
    "stub_dataclass_record",
    "stub_dataclass_nested_fields"
]


def test_method():
    """Test coroutine for /schema/typeV2 route."""

    for module_name in module_names:
        expected_result_file_path = os.path.abspath(__file__).replace(".py", f".{module_name}.expected.json")
        with open(expected_result_file_path, 'r', encoding='utf-8') as file:
            expected_result = json.load(file)

        expected_result_obj = TypeDecl(**expected_result)
        pass


if __name__ == "__main__":
    pytest.main([__file__])
