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
from cl.runtime.storage.sql.sqlite_schema_manager import SqliteSchemaManager
from stubs.cl.runtime import StubDataclassRecordKey, StubDataclassRecord, StubDataclassDerivedRecord, \
    StubDataclassDerivedFromDerivedRecord, StubDataclassDictFields, StubDataclassListDictFields, \
    StubDataclassDictListFields, StubDataclassListFields, StubDataclassOtherDerivedRecord


# TODO (Roman): move to Schema tests
def test_get_subtypes_in_hierarchy():

    types_in_hierarchy = Schema.get_types_in_hierarchy(StubDataclassRecordKey)

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
        assert type_.get_key_type(None) == expected_key_type # noqa


def test_resolve_columns_for_type():

    test_type = StubDataclassDerivedFromDerivedRecord

    expected_columns = [
        'StubDataclassRecord.Id',
        'StubDataclassDerivedRecord.DerivedField',
        'StubDataclassDictFields.StrDict',
        'StubDataclassDictFields.FloatDict',
        'StubDataclassDictFields.DateDict',
        'StubDataclassDictFields.DataDict',
        'StubDataclassDictFields.KeyDict',
        'StubDataclassDictFields.RecordDict',
        'StubDataclassDictFields.DerivedRecordDict',
        'StubDataclassDictListFields.FloatDictList',
        'StubDataclassDictListFields.DateDictList',
        'StubDataclassDictListFields.RecordDictList',
        'StubDataclassDictListFields.DerivedRecordDictList',
        'StubDataclassListDictFields.FloatListDict',
        'StubDataclassListDictFields.DateListDict',
        'StubDataclassListDictFields.RecordListDict',
        'StubDataclassListDictFields.DerivedRecordListDict',
        'StubDataclassListFields.StrList',
        'StubDataclassListFields.FloatList',
        'StubDataclassListFields.DateList',
        'StubDataclassListFields.DataList',
        'StubDataclassListFields.KeyList',
        'StubDataclassListFields.RecordList',
        'StubDataclassListFields.DerivedRecordList',
        'StubDataclassOtherDerivedRecord.OtherDerived',
    ]

    resolved_columns = SqliteSchemaManager()._resolve_columns_for_type(test_type)

    assert expected_columns == resolved_columns


if __name__ == '__main__':
    pytest.main([__file__])
