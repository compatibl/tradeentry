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
from cl.runtime.storage.local.local_cache import LocalCache
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_record import StubDataclassRecord


def test_smoke():
    """Smoke test."""

    # Create an instance of record cache
    cache = LocalCache.instance()

    # Create test record and populate with sample data
    record = StubDataclassRecord()
    key = record.get_key()

    # Test saving and loading
    dataset = None  # TODO: Support datasets "\\sample_dataset"

    # Save a single record
    cache.save_many([record], dataset=dataset)

    loaded_records = cache.load_many(StubDataclassRecord, [record, key, None], dataset=dataset)
    assert loaded_records[0] is record  # Same object is returned without lookup
    assert loaded_records[1] is record  # In case of local cache only, also the same object
    assert loaded_records[2] is None

    assert cache.load_one(StubDataclassRecord, record) is record  # Same object is returned without lookup
    assert cache.load_one(StubDataclassRecord, key) is record  # In case of local cache only, also the same object


if __name__ == "__main__":
    pytest.main([__file__])
