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
from cl.runtime.serialization.flat_dict_serializer import FlatDictSerializer
from stubs.cl.runtime import StubDataclassDerivedFromDerivedRecord
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassDictFields
from stubs.cl.runtime import StubDataclassDictListFields
from stubs.cl.runtime import StubDataclassListDictFields
from stubs.cl.runtime import StubDataclassListFields
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassOptionalFields
from stubs.cl.runtime import StubDataclassOtherDerivedRecord
from stubs.cl.runtime import StubDataclassPrimitiveFields
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime import StubDataclassSingleton


def test_data_serialization():
    sample_types = [
        StubDataclassRecord,
        StubDataclassNestedFields,
        StubDataclassDerivedRecord,
        StubDataclassDerivedFromDerivedRecord,
        StubDataclassOtherDerivedRecord,
        StubDataclassListFields,
        StubDataclassOptionalFields,
        StubDataclassDictFields,
        StubDataclassDictListFields,
        StubDataclassListDictFields,
        StubDataclassPrimitiveFields,
        StubDataclassSingleton,
    ]

    serializer = FlatDictSerializer()

    for sample_type in sample_types:
        obj_1 = sample_type()
        serialized_1 = serializer.serialize_data(obj_1, is_root=True)
        obj_2 = serializer.deserialize_data(serialized_1)
        serialized_2 = serializer.serialize_data(obj_2, is_root=True)

        assert obj_1 == obj_2
        assert serialized_1 == serialized_2


if __name__ == "__main__":
    pytest.main([__file__])
