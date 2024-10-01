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
import sqlite3
from cl.runtime.schema.schema import Schema
from cl.runtime.db.sql.sqlite_db import dict_factory
from cl.runtime.db.sql.sqlite_schema_manager import SqliteSchemaManager
from stubs.cl.runtime import StubDataclassDerivedFromDerivedRecord
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassDictFields
from stubs.cl.runtime import StubDataclassDictListFields
from stubs.cl.runtime import StubDataclassListDictFields
from stubs.cl.runtime import StubDataclassListFields
from stubs.cl.runtime import StubDataclassOtherDerivedRecord
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime import StubDataclassRecordKey


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
        assert type_.get_key_type() == expected_key_type


def test_get_columns_mapping():
    test_type = StubDataclassDerivedFromDerivedRecord

    expected_columns = {
        "_type": "_type",
        "id": "StubDataclassRecordKey.id",
        "derived_field": "StubDataclassDerivedRecord.derived_field",
        "str_dict": "StubDataclassDictFields.str_dict",
        "float_dict": "StubDataclassDictFields.float_dict",
        "date_dict": "StubDataclassDictFields.date_dict",
        "data_dict": "StubDataclassDictFields.data_dict",
        "key_dict": "StubDataclassDictFields.key_dict",
        "record_dict": "StubDataclassDictFields.record_dict",
        "derived_record_dict": "StubDataclassDictFields.derived_record_dict",
        "float_dict_list": "StubDataclassDictListFields.float_dict_list",
        "date_dict_list": "StubDataclassDictListFields.date_dict_list",
        "record_dict_list": "StubDataclassDictListFields.record_dict_list",
        "derived_record_dict_list": "StubDataclassDictListFields.derived_record_dict_list",
        "float_list_dict": "StubDataclassListDictFields.float_list_dict",
        "date_list_dict": "StubDataclassListDictFields.date_list_dict",
        "record_list_dict": "StubDataclassListDictFields.record_list_dict",
        "derived_record_list_dict": "StubDataclassListDictFields.derived_record_list_dict",
        "str_list": "StubDataclassListFields.str_list",
        "float_list": "StubDataclassListFields.float_list",
        "date_list": "StubDataclassListFields.date_list",
        "data_list": "StubDataclassListFields.data_list",
        "key_list": "StubDataclassListFields.key_list",
        "record_list": "StubDataclassListFields.record_list",
        "derived_record_list": "StubDataclassListFields.derived_record_list",
        "other_derived": "StubDataclassOtherDerivedRecord.other_derived",
    }

    resolved_columns = SqliteSchemaManager().get_columns_mapping(test_type)

    assert expected_columns == resolved_columns


if __name__ == "__main__":
    pytest.main([__file__])
