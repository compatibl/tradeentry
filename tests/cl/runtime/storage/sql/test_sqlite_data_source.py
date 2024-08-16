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

import time

import pytest
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
from typing import Any
from typing import Iterable

from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_primitive_fields_key import StubDataclassPrimitiveFieldsKey


def _assert_equals_iterable_without_ordering(iterable: Iterable[Any], other_iterable: Iterable[Any]) -> bool:
    iterable_as_list = list(iterable) if not isinstance(iterable, list) else iterable
    other_iterable_as_list = list(other_iterable) if not isinstance(other_iterable, list) else other_iterable

    if len(iterable_as_list) != len(other_iterable_as_list):
        raise ValueError(f"Iterables have different length: {len(iterable_as_list)} and {len(other_iterable_as_list)}")

    for item in iterable_as_list:
        if item not in other_iterable_as_list:
            raise ValueError(f"Item {item} contains only in first iterable.")

    return True


def test_smoke():
    data_source = SqliteDataSource(data_source_id="default")
    record = StubDataclassRecord()

    data_source.save_many([record, record])

    loaded_records = list(data_source.load_many([record.get_key()]))
    assert len(loaded_records) == 1
    assert loaded_records[0] == record


def test_complex_records():
    samples = [
        StubDataclassRecord(id="abc1"),
        StubDataclassNestedFields(primitive="abc2"),
        StubDataclassDerivedRecord(id="abc3"),
        StubDataclassDerivedFromDerivedRecord(id="abc4"),
        # StubDataclassOtherDerivedRecord(id="abc5"),
        # StubDataclassListFields(id="abc6"),
        # StubDataclassOptionalFields(id="abc7"),
        # StubDataclassDictFields(id="abc8"),
        # StubDataclassDictListFields(id="abc9"),
        # StubDataclassListDictFields(id="abc10"),
        StubDataclassPrimitiveFields(key_str_field="abc11"),
        # StubDataclassSingleton(),
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
        StubDataclassRecord(id="abc1"),
        StubDataclassNestedFields(primitive="abc2"),
        StubDataclassDerivedRecord(id="abc3"),
        StubDataclassDerivedFromDerivedRecord(id="abc4"),
        StubDataclassOtherDerivedRecord(id="abc5"),
        StubDataclassListFields(id="abc6"),
        StubDataclassOptionalFields(id="abc7"),
        StubDataclassDictFields(id="abc8"),
        StubDataclassDictListFields(id="abc9"),
        StubDataclassListDictFields(id="abc10"),
        StubDataclassPrimitiveFields(key_str_field="abc11"),
    ]

    sample_keys = [x.get_key() for x in samples]

    data_source = SqliteDataSource(data_source_id="default")

    try:
        # load from non-existing tables
        loaded_records = list(data_source.load_many(sample_keys))
        assert loaded_records == [None] * len(samples)

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
        assert loaded_records == [None] * len(samples)

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


def test_load_all():
    base_samples = [
        StubDataclassRecord(id="base1"),
        StubDataclassRecord(id="base2"),
        StubDataclassRecord(id="base3"),
    ]

    derived_samples = [
        StubDataclassDerivedRecord(id="derived1"),
        StubDataclassDerivedFromDerivedRecord(id="derived2"),
    ]

    other_derived_samples = [
        StubDataclassOtherDerivedRecord(id="derived3"),
    ]

    all_samples = base_samples + derived_samples + other_derived_samples
    data_source = SqliteDataSource(data_source_id="default")

    try:
        data_source.save_many(all_samples)

        loaded_records = data_source.load_all(StubDataclassRecord)
        assert _assert_equals_iterable_without_ordering(all_samples, loaded_records)

        loaded_records = data_source.load_all(StubDataclassDerivedRecord)
        assert _assert_equals_iterable_without_ordering(derived_samples, loaded_records)

    finally:
        data_source.delete_db()


def test_performance():

    samples = [StubDataclassPrimitiveFields(key_str_field=f"key{i}") for i in range(1000)]
    sample_keys = [sample.get_key() for sample in samples]
    data_source = SqliteDataSource(data_source_id="default")
    try:
        start_time = time.time()
        data_source.save_many(samples)
        end_time = time.time()

        print(f"Save many bulk: {end_time - start_time}s.")

        start_time = time.time()
        for sample in samples:
            data_source.save_one(sample)
        end_time = time.time()
        print(f"Save many one by one: {end_time - start_time}s.")

        start_time = time.time()
        list(data_source.load_many(sample_keys))
        end_time = time.time()
        print(f"Load many bulk: {end_time - start_time}s.")

        start_time = time.time()
        for key in sample_keys:
            data_source.load_one(key)
        end_time = time.time()
        print(f"Load many one by one: {end_time - start_time}s.")

        for n in range(10000, 100000, 10000):
            try:
                data_source.load_many([StubDataclassPrimitiveFieldsKey(key_str_field=f"key{i}") for i in range(n)])
            except Exception:
                max_n = n
                break

            max_n = n

        print(f"Max number of keys in request: {max_n}.")
    finally:
        data_source.delete_db()


if __name__ == "__main__":
    pytest.main([__file__])
