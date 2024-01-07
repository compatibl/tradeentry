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
from cl.runtime.data.no_key.stubs.stub_no_key_record import StubNoKeyRecord


def test_smoke():
    """Smoke test."""

    # Create test base_record and populate with sample data
    context = rt.Context()
    base_record = StubNoKeyRecord.create(context)

    # Test that context has been set
    assert base_record.context == context

    # Test type and key
    table_name = base_record.get_table()
    assert table_name == f"{type(base_record).__module__}.{type(base_record).__name__}"
    key = base_record.get_key()
    assert key == 'abc;123'

    # Test roundtrip serialization
    base_record_dict = base_record.to_dict()
    base_record_clone = StubNoKeyRecord.from_dict(base_record_dict)
    base_record_clone_dict = base_record_clone.to_dict()
    assert len(base_record_dict) == 4
    assert base_record_dict == base_record_clone_dict


if __name__ == '__main__':
    pytest.main([__file__])
