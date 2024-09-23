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
from cl.runtime.testing.regression_guard import RegressionGuard
from cl.runtime.schema.for_dataclasses.dataclass_type_decl import DataclassTypeDecl
from stubs.cl.runtime import StubDataclassListFields
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassPrimitiveFields
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_optional_fields import StubDataclassOptionalFields


def test_method():
    """Test coroutine for /schema/typeV2 route."""

    sample_types = [
        StubDataclassRecord,
        StubDataclassPrimitiveFields,
        StubDataclassListFields,
        StubDataclassNestedFields,
        StubDataclassOptionalFields,
    ]

    for sample_type in sample_types:
        result_obj = DataclassTypeDecl.for_type(sample_type)
        result_dict = result_obj.to_type_decl_dict()

        guard = RegressionGuard(channel=sample_type.__module__.rsplit(".", maxsplit=1)[1])
        guard.write(result_dict)

    RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
