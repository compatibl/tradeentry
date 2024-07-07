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
from cl.runtime.serialization.slots_key_serializer import SlotsKeySerializer
from stubs.cl.runtime import StubDataclassListFields
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassOptionalFields
from stubs.cl.runtime import StubDataclassPrimitiveFields
from stubs.cl.runtime import StubDataclassRecord


def test_smoke():
    """Test coroutine for /schema/typeV2 route."""

    sample_types = [
        StubDataclassRecord,
        StubDataclassPrimitiveFields,
        StubDataclassListFields,
        StubDataclassNestedFields,
        StubDataclassOptionalFields,
    ]

    key_serializer = SlotsKeySerializer()

    for sample_type in sample_types:
        obj_1 = sample_type()
        serialized_1 = key_serializer.serialize_key(obj_1)
        serialized_2 = key_serializer.serialize_key(obj_1.get_key())

        assert serialized_1 == serialized_2


if __name__ == "__main__":
    pytest.main([__file__])
