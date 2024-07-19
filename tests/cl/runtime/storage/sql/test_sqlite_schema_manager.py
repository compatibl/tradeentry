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
import sqlite3

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


def test_get_columns_mapping():

    test_type = StubDataclassDerivedFromDerivedRecord

    expected_columns = {
        "Id": "StubDataclassRecord.Id",
        "DerivedField": "StubDataclassDerivedRecord.DerivedField",
        "StrDict": "StubDataclassDictFields.StrDict",
        "FloatDict": "StubDataclassDictFields.FloatDict",
        "DateDict": "StubDataclassDictFields.DateDict",
        "DataDict": "StubDataclassDictFields.DataDict",
        "KeyDict": "StubDataclassDictFields.KeyDict",
        "RecordDict": "StubDataclassDictFields.RecordDict",
        "DerivedRecordDict": "StubDataclassDictFields.DerivedRecordDict",
        "FloatDictList": "StubDataclassDictListFields.FloatDictList",
        "DateDictList": "StubDataclassDictListFields.DateDictList",
        "RecordDictList": "StubDataclassDictListFields.RecordDictList",
        "DerivedRecordDictList": "StubDataclassDictListFields.DerivedRecordDictList",
        "FloatListDict": "StubDataclassListDictFields.FloatListDict",
        "DateListDict": "StubDataclassListDictFields.DateListDict",
        "RecordListDict": "StubDataclassListDictFields.RecordListDict",
        "DerivedRecordListDict": "StubDataclassListDictFields.DerivedRecordListDict",
        "StrList": "StubDataclassListFields.StrList",
        "FloatList": "StubDataclassListFields.FloatList",
        "DateList": "StubDataclassListFields.DateList",
        "DataList": "StubDataclassListFields.DataList",
        "KeyList": "StubDataclassListFields.KeyList",
        "RecordList": "StubDataclassListFields.RecordList",
        "DerivedRecordList": "StubDataclassListFields.DerivedRecordList",
        "OtherDerived": "StubDataclassOtherDerivedRecord.OtherDerived",
    }

    resolved_columns = SqliteSchemaManager().get_columns_mapping(test_type)

    assert expected_columns == resolved_columns


def test_create_table():
    connection = sqlite3.connect('test_sqlite_db.sqlite')

    with connection as connection:
        sqlite_schema_manager = SqliteSchemaManager(sqlite_connection=connection)

        existing_tables = sqlite_schema_manager.existing_tables()
        assert existing_tables == []

        table_name = sqlite_schema_manager.table_name_for_type(StubDataclassRecord)
        columns = sqlite_schema_manager.get_columns_mapping(StubDataclassRecord).values()
        sqlite_schema_manager.create_table(table_name, columns)

        existing_tables = sqlite_schema_manager.existing_tables()
        assert existing_tables == [StubDataclassRecord.__name__]

        sqlite_schema_manager.delete_table_by_name(StubDataclassRecord.__name__)
        existing_tables = sqlite_schema_manager.existing_tables()
        assert existing_tables == []


if __name__ == '__main__':
    pytest.main([__file__])
