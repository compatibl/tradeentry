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
from cl.runtime.serialization.string_serializer import StringSerializer
from stubs.cl.runtime import StubDataclassListFields
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassOptionalFields
from stubs.cl.runtime import StubDataclassPrimitiveFields
from stubs.cl.runtime import StubDataclassRecord


def test_dataset_serialization():
    """Test dataset serialization."""

    serializer = StringSerializer()

    assert serializer.serialize_dataset(None) == ""
    assert serializer.serialize_dataset("abc") == "abc"
    assert serializer.serialize_dataset("abc\\def") == "abc\\def"
    assert serializer.serialize_dataset(("abc", "def")) == "abc\\def"
    assert serializer.serialize_dataset(("abc", ("def", "xyz"))) == "abc\\def\\xyz"
    assert serializer.serialize_dataset(("abc", ("def", 123.456))) == "abc\\def\\123.456"


def test_key_serialization():
    """Test key serialization."""

    sample_types = [
        StubDataclassRecord,
        # StubDataclassPrimitiveFields,
        # StubDataclassListFields,
        # StubDataclassNestedFields,
        # StubDataclassOptionalFields,
    ]

    key_serializer = StringSerializer()

    for sample_type in sample_types:
        obj_1 = sample_type()
        obj_1_key = obj_1.get_key()
        serialized_1 = key_serializer.serialize_key(obj_1)
        serialized_2 = key_serializer.serialize_key(obj_1_key)

        assert serialized_1 == serialized_2

        deserialized_key_1 = key_serializer.deserialize_key(serialized_1, sample_type.get_key_type(None))
        deserialized_key_2 = key_serializer.deserialize_key(serialized_2, sample_type.get_key_type(None))
        assert obj_1_key == deserialized_key_1 == deserialized_key_2


if __name__ == "__main__":
    pytest.main([__file__])
