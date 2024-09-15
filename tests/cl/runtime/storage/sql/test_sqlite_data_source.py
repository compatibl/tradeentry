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
import time
from typing import Any
from typing import Iterable
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.records.class_info import ClassInfo
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
    data_source_class = ClassInfo.get_class_path(SqliteDataSource)
    with TestingContext(data_source_class=data_source_class) as context:
        record = StubDataclassRecord()
        context.save_many([record, record])

        loaded_records = list(context.load_many(StubDataclassRecord, [record.get_key()]))
        assert len(loaded_records) == 1
        assert loaded_records[0] == record


def test_complex_records():
    data_source_class = ClassInfo.get_class_path(SqliteDataSource)
    with TestingContext(data_source_class=data_source_class) as context:
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
            StubDataclassSingleton(),
        ]

        context.save_many(samples)

        sample_keys = [sample.get_key() for sample in samples]
        loaded_records = [context.load_one(type(key), key) for key in sample_keys]

        assert loaded_records == samples


def test_basic_operations():
    data_source_class = ClassInfo.get_class_path(SqliteDataSource)
    with TestingContext(data_source_class=data_source_class) as context:
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

        # Load from empty tables
        loaded_records = [context.load_one(type(key), key) for key in sample_keys]
        assert loaded_records == [None] * len(samples)

        # Populate tables
        context.save_many(samples)

        # Load one by one for all keys because each type is different
        loaded_records = [context.load_one(type(key), key) for key in sample_keys]
        assert loaded_records == samples

        # Delete first and last record
        context.delete_many([sample_keys[0], sample_keys[-1]])
        loaded_records = [context.load_one(type(key), key) for key in sample_keys]
        assert loaded_records == [None, *samples[1:-1], None]

        # Delete all records
        context.delete_many(sample_keys)
        loaded_records = [context.load_one(type(key), key) for key in sample_keys]
        assert loaded_records == [None] * len(samples)


def test_record_upsert():
    data_source_class = ClassInfo.get_class_path(SqliteDataSource)
    with TestingContext(data_source_class=data_source_class) as context:
        # create sample and save
        sample = StubDataclassRecord()
        context.save_one(sample)
        loaded_record = context.load_one(StubDataclassRecord, sample.get_key())
        assert loaded_record == sample

        # create sample with the same key and save
        override_sample = StubDataclassDerivedRecord()
        context.save_one(override_sample)
        loaded_record = context.load_one(StubDataclassDerivedRecord, sample.get_key())
        assert loaded_record == override_sample

        override_sample = StubDataclassDerivedFromDerivedRecord()
        context.save_one(override_sample)
        loaded_record = context.load_one(StubDataclassDerivedFromDerivedRecord, sample.get_key())
        assert loaded_record == override_sample


def test_load_all():
    data_source_class = ClassInfo.get_class_path(SqliteDataSource)
    with TestingContext(data_source_class=data_source_class) as context:
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

        context.save_many(all_samples)

        loaded_records = context.load_all(StubDataclassRecord)
        assert _assert_equals_iterable_without_ordering(all_samples, loaded_records)

        loaded_records = context.load_all(StubDataclassDerivedRecord)
        assert _assert_equals_iterable_without_ordering(derived_samples, loaded_records)


@pytest.mark.skip("Performance test.")
def test_performance():
    data_source_class = ClassInfo.get_class_path(SqliteDataSource)
    with TestingContext(data_source_class=data_source_class) as context:
        n = 1000
        samples = [StubDataclassPrimitiveFields(key_str_field=f"key{i}") for i in range(n)]
        sample_keys = [sample.get_key() for sample in samples]

        print(f">>> Test stub type: {StubDataclassPrimitiveFields.__name__}, {n=}.")
        start_time = time.time()
        context.save_many(samples)
        end_time = time.time()

        print(f"Save many bulk: {end_time - start_time}s.")

        start_time = time.time()
        for sample in samples:
            context.save_one(sample)
        end_time = time.time()
        print(f"Save many one by one: {end_time - start_time}s.")

        start_time = time.time()
        list(context.load_many(sample_keys))
        end_time = time.time()
        print(f"Load many bulk: {end_time - start_time}s.")

        start_time = time.time()
        for key in sample_keys:
            context.load_one(type(key), key)
        end_time = time.time()
        print(f"Load many one by one: {end_time - start_time}s.")


def test_singleton():
    data_source_class = ClassInfo.get_class_path(SqliteDataSource)
    with TestingContext(data_source_class=data_source_class) as context:
        singleton_sample = StubDataclassSingleton()
        context.save_one(singleton_sample)
        loaded_sample = context.load_one(StubDataclassSingleton, singleton_sample.get_key())
        assert loaded_sample == singleton_sample

        other_singleton_sample = StubDataclassSingleton(str_field="other")
        context.save_one(other_singleton_sample)
        all_records = list(context.load_all(other_singleton_sample.__class__))
        assert len(all_records) == 1
        assert all_records[0] == other_singleton_sample


if __name__ == "__main__":
    pytest.main([__file__])
