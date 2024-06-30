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
import json
import os
import pytest
from cl.runtime.schema.dataclasses.dataclass_type_decl import DataclassTypeDecl
from cl.runtime.schema.type_decl import TypeDecl
from stubs.cl.runtime import StubDataclassNestedFields, StubCustomBase, StubDataclassListFields, \
    StubDataclassPrimitiveFields
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.records.dataclasses.stub_dataclass_optional_fields import StubDataclassOptionalFields


def test_method():
    """Test coroutine for /schema/typeV2 route."""

    sample_types = [
        StubDataclassRecord,
        StubDataclassPrimitiveFields,
        StubDataclassListFields,
        StubDataclassNestedFields,
        StubDataclassOptionalFields
    ]

    for sample_type in sample_types:
        class_module = sample_type.__module__.rsplit(".", maxsplit=1)[1]
        received_result_file_path = os.path.abspath(__file__).replace(".py", f".{class_module}.received.json")
        expected_result_file_path = os.path.abspath(__file__).replace(".py", f".{class_module}.expected.json")

        result_obj = DataclassTypeDecl.for_type(sample_type)
        result_dict = result_obj.to_type_decl_dict()

        # Save the dictionary to a file
        with open(received_result_file_path, 'w') as received_result_file:
            json.dump(result_dict, received_result_file, indent=4)

        # Load expected result from a file
        with open(expected_result_file_path, "r", encoding="utf-8") as expected_result_file:
            expected_result_dict = json.load(expected_result_file)

        # Compare
        assert result_dict == expected_result_dict
        pass


if __name__ == "__main__":
    pytest.main([__file__])
