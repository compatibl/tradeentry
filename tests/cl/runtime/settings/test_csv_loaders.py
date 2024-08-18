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
from pathlib import Path

from cl.runtime.loaders.csv_dir_loader import CsvDirLoader
from cl.runtime.storage.local.local_cache import LocalCache

from cl.runtime.loaders.csv_file_loader import CsvFileLoader
from cl.runtime.settings.preload_settings import PreloadSettings
from stubs.cl.runtime import StubDataclassDerivedRecord, StubDataclassRecordKey, StubDataclassRecord


def test_csv_file_loader():
    """Test CsvFileLoader class."""

    # Create a new instance of cache for the test
    cache = LocalCache()

    file_path = str(Path(__file__).parent / "StubDataclassDerivedRecord.csv")
    file_loader = CsvFileLoader(record_type=StubDataclassDerivedRecord, file_path=file_path)
    file_loader.load(cache)

    # Verify
    # TODO: Check count using load_all or count method of DataSource when created
    for i in range(1, 2):
        record = cache.load_one(StubDataclassRecordKey(id=f"derived_id_{i}"))
        assert record == StubDataclassDerivedRecord(id=f"derived_id_{i}", derived_field=f"test_derived_field_value_{i}")


def test_csv_dir_loader():
    """Test CsvDirLoader class."""

    # Create a new instance of cache for the test
    cache = LocalCache()

    dir_path = str(Path(__file__).parent)
    dir_loader = CsvDirLoader(dir_path=dir_path)
    dir_loader.load(cache)

    # Verify
    # TODO: Check count using load_all or count method of DataSource when created
    for i in range(1, 2):
        record = cache.load_one(StubDataclassRecordKey(id=f"base_id_{i}"))
        assert record == StubDataclassRecord(id=f"base_id_{i}")
    for i in range(1, 2):
        record = cache.load_one(StubDataclassRecordKey(id=f"derived_id_{i}"))
        assert record == StubDataclassDerivedRecord(id=f"derived_id_{i}", derived_field=f"test_derived_field_value_{i}")


if __name__ == "__main__":
    pytest.main([__file__])
