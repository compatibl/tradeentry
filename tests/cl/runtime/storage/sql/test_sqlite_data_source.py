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
from collections import defaultdict

import pytest

from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.storage.sql.sqlite_data_source import SqliteDataSource

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


def test_smoke():
    data_source = SqliteDataSource(data_source_id="default")
    record = StubDataclassRecord()

    data_source.save_many([record, record])

    loaded_records = list(data_source.load_many([record.get_key()]))
    assert len(loaded_records) == 1
    assert loaded_records[0] == record


def test_complex_records():
    samples = [
        StubDataclassRecord(id='abc1'),
        StubDataclassNestedFields(primitive='abc2'),
        StubDataclassDerivedRecord(id='abc3'),
        StubDataclassDerivedFromDerivedRecord(id='abc4'),
        StubDataclassOtherDerivedRecord(id='abc5'),
        StubDataclassListFields(id='abc6'),
        StubDataclassOptionalFields(id='abc7'),
        StubDataclassDictFields(id='abc8'),
        StubDataclassDictListFields(id='abc9'),
        StubDataclassListDictFields(id='abc10'),
        StubDataclassPrimitiveFields(key_str_field='abc11'),
        StubDataclassSingleton(),
    ]

    data_source = SqliteDataSource(data_source_id="default")

    try:
        data_source.save_many(samples)

        sample_keys = [sample.get_key() for sample in samples]
        loaded_records = list(data_source.load_many(sample_keys))

        assert loaded_records == samples

    finally:
        data_source.delete_db()


def test_basic_operations():
    samples = [
        StubDataclassRecord(id='abc1'),
        StubDataclassNestedFields(primitive='abc2'),
        StubDataclassDerivedRecord(id='abc3'),
        StubDataclassDerivedFromDerivedRecord(id='abc4'),
        StubDataclassOtherDerivedRecord(id='abc5'),
        StubDataclassListFields(id='abc6'),
        StubDataclassOptionalFields(id='abc7'),
        StubDataclassDictFields(id='abc8'),
        StubDataclassDictListFields(id='abc9'),
        StubDataclassListDictFields(id='abc10'),
        StubDataclassPrimitiveFields(key_str_field='abc11'),
    ]

    sample_keys = [x.get_key() for x in samples]

    data_source = SqliteDataSource(data_source_id="default")

    try:

        # load from non-existing tables
        loaded_records = list(data_source.load_many(sample_keys))
        assert loaded_records == [None]*len(samples)

        data_source.save_many(samples)

        # load many for all keys
        loaded_records = list(data_source.load_many(sample_keys))
        assert loaded_records == samples

        # load one by one for all keys
        loaded_records = [data_source.load_one(key) for key in sample_keys]
        assert loaded_records == samples

        # delete first and last key
        data_source.delete_many([sample_keys[0], sample_keys[-1]])
        loaded_records = list(data_source.load_many(sample_keys))
        assert loaded_records == [None, *samples[1:-1], None]

        # delete all keys
        data_source.delete_many(sample_keys)
        loaded_records = list(data_source.load_many(sample_keys))
        assert loaded_records == [None]*len(samples)

    finally:
        data_source.delete_db()


def test_record_upsert():

    data_source = SqliteDataSource(data_source_id="default")

    try:
        # create sample and save
        sample = StubDataclassRecord()
        data_source.save_one(sample)
        loaded_record = data_source.load_one(sample.get_key())
        assert loaded_record == sample

        # create sample with the same key and save
        override_sample = StubDataclassDerivedRecord()
        data_source.save_one(override_sample)
        loaded_record = data_source.load_one(sample.get_key())
        assert loaded_record == override_sample

        override_sample = StubDataclassDerivedFromDerivedRecord()
        data_source.save_one(override_sample)
        loaded_record = data_source.load_one(sample.get_key())
        assert loaded_record == override_sample

    finally:
        data_source.delete_db()


if __name__ == '__main__':
    pytest.main([__file__])
