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
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.db.mongo.basic_mongo_data_source import BasicMongoDataSource
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_record import StubDataclassRecord


@pytest.mark.skip("Requires MongoDB server.")  # TODO: Switch test to MongoMock
def test_check_data_source_id():
    """Test '_get_db_name' method."""

    with TestingContext() as context:
        # Check for length
        BasicMongoDataSource.check_data_source_id("a" * 63)
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id("a" * 64)

        # Letters, numbers and underscore are allowed
        BasicMongoDataSource.check_data_source_id("abc")
        BasicMongoDataSource.check_data_source_id("123")
        BasicMongoDataSource.check_data_source_id("abc_xyz")

        # Semicolon is allowed even though it is not in the suggested list
        BasicMongoDataSource.check_data_source_id("abc;xyz")

        # Check for space
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id("abc xyz")
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id("abc ")
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id(" xyz")

        # Check for period
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id("abc.xyz")
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id("abc.")
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id(".xyz")

        # Check for other symbols
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id("abc:xyz")
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id("abc|xyz")
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id("abc\\xyz")
        with pytest.raises(RuntimeError):
            BasicMongoDataSource.check_data_source_id("abc/xyz")


@pytest.mark.skip("Requires MongoDB server.")  # TODO: Switch test to MongoMock
def test_load_filter():
    """Test 'load_filter' method."""

    data_source_class = ClassInfo.get_class_path(BasicMongoDataSource)
    with TestingContext(data_source_class=data_source_class) as context:
        # Create test record and populate with sample data
        offset = 0
        matching_records = [StubDataclassDerivedRecord(id=str(offset + i), derived_field="a") for i in range(2)]
        offset = len(matching_records)
        non_matching_records = [StubDataclassDerivedRecord(id=str(offset + i), derived_field="b") for i in range(2)]
        context.save_many(matching_records + non_matching_records)

        filter_obj = StubDataclassDerivedRecord(id=None, derived_field="a")
        loaded_records = context.load_filter(StubDataclassDerivedRecord, filter_obj)
        assert len(loaded_records) == len(matching_records)
        assert all(x.derived_field == filter_obj.derived_field for x in loaded_records)


@pytest.mark.skip("Requires MongoDB server.")  # TODO: Switch test to MongoMock
def test_smoke():
    """Smoke test."""

    # TODO: Do not hardcode DB name
    data_source_class = ClassInfo.get_class_path(BasicMongoDataSource)
    with TestingContext(data_source_class=data_source_class) as context:
        # Create test record and populate with sample data
        record = StubDataclassRecord()
        key = record.get_key()

        # Save a single record
        context.save_many([record])

        # Load using record or key
        loaded_records = context.load_many(StubDataclassRecord, [record, key, None])
        assert loaded_records[0] is record  # Same object is returned without lookup
        assert loaded_records[1] == record  # Not the same object but equal
        assert loaded_records[2] is None

        assert context.load_one(StubDataclassRecord, record) is record  # Same object is returned without lookup
        assert context.load_one(StubDataclassRecord, key) == record  # Not the same object but equal


if __name__ == "__main__":
    pytest.main([__file__])
