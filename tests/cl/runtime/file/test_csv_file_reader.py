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
import os
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.file.csv_file_reader import CsvFileReader
from cl.runtime.settings.settings import Settings
from cl.runtime.storage.local.local_cache import LocalCache
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime import StubDataclassRecordKey


def test_smoke():
    """Test CsvFileReader class."""

    project_root = Settings.get_project_root()
    file_path = os.path.join(project_root, "preloads/stubs/cl/runtime/csv/StubDataclassDerivedRecord.csv")

    # Create a new instance of local cache for the test
    with TestingContext() as context:
        # TODO: Change the API not to take record type or make it optional
        file_reader = CsvFileReader(record_type=StubDataclassDerivedRecord, file_path=file_path)
        file_reader.read()

        # Verify
        # TODO: Check count using load_all or count method of DataSource when created
        for i in range(1, 2):
            key = StubDataclassRecordKey(id=f"derived_id_{i}")
            record = context.load_one(StubDataclassRecord, key)
            assert record == StubDataclassDerivedRecord(
                id=f"derived_id_{i}", derived_field=f"test_derived_field_value_{i}"
            )


if __name__ == "__main__":
    pytest.main([__file__])
