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

import os
import pytest
from cl.runtime.context.context import Context
from cl.runtime.file.csv_dir_reader import CsvDirReader
from cl.runtime.settings.settings import Settings
from cl.runtime.storage.local.local_cache import LocalCache
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime import StubDataclassRecordKey


def test_smoke():
    """Test CsvDirReader class."""

    project_root = Settings.get_project_root()
    dir_path = os.path.join(project_root, "preload/stubs/cl/runtime/csv")

    # Create a new instance of local cache for the test
    data_source = LocalCache()
    with Context(data_source=data_source):
        dir_reader = CsvDirReader(dir_path=dir_path)
        dir_reader.read()

        # Verify
        # TODO: Check count using load_all or count method of DataSource when created
        for i in range(1, 2):
            record = data_source.load_one(StubDataclassRecordKey(id=f"base_id_{i}"))
            assert record == StubDataclassRecord(id=f"base_id_{i}")
        for i in range(1, 2):
            record = data_source.load_one(StubDataclassRecordKey(id=f"derived_id_{i}"))
            assert record == StubDataclassDerivedRecord(
                id=f"derived_id_{i}", derived_field=f"test_derived_field_value_{i}"
            )


if __name__ == "__main__":
    pytest.main([__file__])
