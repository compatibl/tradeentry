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
from cl.runtime.context.env_util import EnvUtil
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.file.csv_file_reader import CsvFileReader
from stubs.cl.runtime import StubDataclassComposite
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime import StubDataclassRecordKey


def test_csv_file_reader():
    """Test CsvFileReader class."""

    # Create a new instance of local cache for the test
    with TestingContext() as context:
        env_dir = EnvUtil.get_env_dir()
        file_path = os.path.join(env_dir, "StubDataclassDerivedRecord.csv")
        # TODO: Change the API not to take record type or make it optional
        file_reader = CsvFileReader(file_path=file_path)
        file_reader.read_and_save()

        file_path = os.path.join(env_dir, "StubDataclassNestedFields.csv")
        file_reader = CsvFileReader(file_path=file_path)
        file_reader.read_and_save()

        file_path = os.path.join(env_dir, "StubDataclassComposite.csv")
        file_reader = CsvFileReader(file_path=file_path)
        file_reader.read_and_save()

        # Verify
        # TODO: Check count using load_all or count method of Db when created
        for i in range(1, 3):
            key = StubDataclassRecordKey(id=f"derived_id_{i}")
            record = context.load_one(StubDataclassRecord, key)
            assert record == StubDataclassDerivedRecord(
                id=f"derived_id_{i}", derived_str_field=f"test_derived_str_field_value_{i}"
            )

        for i in range(1, 4):
            expected_record = StubDataclassNestedFields(
                id=f"nested_{i}",
            )
            record = context.load_one(StubDataclassNestedFields, expected_record.get_key())
            assert record == expected_record

        for i in range(1, 4):
            expected_record = StubDataclassComposite(
                primitive=f"nested_primitive_{i}",
                embedded_1=StubDataclassRecordKey(id=f"embedded_key_id_{i}a"),
                embedded_2=StubDataclassRecordKey(id=f"embedded_key_id_{i}b"),
            )
            record = context.load_one(StubDataclassComposite, expected_record.get_key())
            assert record == expected_record


if __name__ == "__main__":
    pytest.main([__file__])
