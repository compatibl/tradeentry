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

from cl.runtime.schema.schema import Schema
from stubs.cl.runtime import StubDataclassRecordKey, StubDataclassRecord, StubDataclassDerivedRecord, \
    StubDataclassDerivedFromDerivedRecord, StubDataclassDictFields, StubDataclassListDictFields, \
    StubDataclassDictListFields, StubDataclassListFields, StubDataclassOtherDerivedRecord


# TODO (Roman): move to Schema tests
def test_get_subtypes_in_hierarchy():

    types_in_hierarchy = Schema.get_subtypes_in_hierarchy(StubDataclassRecordKey)

    expected_types = {
        StubDataclassRecord,
        StubDataclassDerivedRecord,
        StubDataclassDerivedFromDerivedRecord,
        StubDataclassDictFields,
        StubDataclassDictListFields,
        StubDataclassListDictFields,
        StubDataclassListFields,
        StubDataclassOtherDerivedRecord,
    }

    assert len(types_in_hierarchy) == len(expected_types)
    assert set(types_in_hierarchy) == expected_types


# TODO (Roman): move to Schema tests
def test_get_key_class():

    test_subtypes = (
        StubDataclassRecord,
        StubDataclassDerivedRecord,
        StubDataclassDerivedFromDerivedRecord,
        StubDataclassDictFields,
        StubDataclassDictListFields,
        StubDataclassListDictFields,
        StubDataclassListFields,
        StubDataclassOtherDerivedRecord,
    )

    expected_key_type = StubDataclassRecordKey

    for type_ in test_subtypes:
        assert Schema.get_key_class(type_) == expected_key_type


if __name__ == '__main__':
    pytest.main([__file__])
