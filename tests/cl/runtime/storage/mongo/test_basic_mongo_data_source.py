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

import mongomock
import pytest
from cl.runtime.context.context import Context
from cl.runtime.storage.mongo.basic_mongo_data_source import BasicMongoDataSource
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_record import StubDataclassRecord


def test_smoke():
    """Smoke test."""

    with Context():
        data_source = BasicMongoDataSource(
            _client=mongomock.MongoClient(), data_source_id="default", db_name="Dev;Runtime;V2"
        )

        # Create test record and populate with sample data
        record = StubDataclassRecord()
        key = record.get_key()

        # Save a single record
        data_source.save_many([record])

        # Load using record or key
        loaded_records = data_source.load_many(StubDataclassRecord, [record, key, None])
        assert loaded_records[0] is record  # Same object is returned without lookup
        assert loaded_records[1] == record  # Not the same object but equal
        assert loaded_records[2] is None

        assert data_source.load_one(StubDataclassRecord, record) is record  # Same object is returned without lookup
        assert data_source.load_one(StubDataclassRecord, key) == record  # Not the same object but equal


if __name__ == "__main__":
    pytest.main([__file__])
