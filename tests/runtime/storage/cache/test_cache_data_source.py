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

import cl.runtime as rt
from stubs.runtime.storage.stub_record import StubRecord


# Tests for CacheDataSource


def test_smoke():
    """Smoke test."""

    # Create data source and dataset
    data_source = rt.CacheDataSource()
    data_set = "sample"

    # Create test record and populate with sample data
    context = rt.Context()
    record = StubRecord.create_sample_record(context)
    key = record.get_key()
    record_dict = record.to_dict()

    # Test saving and loading
    data_source.save_one(record, data_set)
    records = data_source.load_many(StubRecord, [key, record], data_set)
    record_from_str_key = data_source.load_one(StubRecord, key, data_set)
    record_from_record_as_key = data_source.load_one(StubRecord, record, data_set)

    # Check loaded record
    loaded_record_dict = record_from_str_key.to_dict()
    assert loaded_record_dict == record_dict

    # TODO - check that when loading by record key it is the same instance


if __name__ == '__main__':
    pytest.main([__file__])
