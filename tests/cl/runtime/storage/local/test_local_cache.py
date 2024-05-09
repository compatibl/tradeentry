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

import dataclasses
import pytest
from cl.runtime import DataSource
from cl.runtime.rest.basic_context import BasicContext
from stubs.cl.runtime.records.dataclasses.stub_dataclass_base import StubDataclassBase


def test_smoke():
    """Smoke test."""

    with BasicContext() as context:
        # Create test record and populate with sample data
        record = StubDataclassBase()
        key = record.get_key()
        record_pack = record.pack()

        # Test saving and loading
        dataset = "sample"
        DataSource.default().save_many([record_pack], dataset)
        loaded_records = StubDataclassBase.load_many([record, key, None], dataset, context=context)

        assert loaded_records[0] == record
        assert loaded_records[1] == record
        assert loaded_records[2] is None


if __name__ == "__main__":
    pytest.main([__file__])
