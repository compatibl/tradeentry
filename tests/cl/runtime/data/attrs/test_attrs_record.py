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
from cl.runtime.data.attrs.stubs.stub_attrs_simple_record import StubAttrsSimpleRecord


def test_smoke():
    """Smoke test."""

    # Create and test standalone key
    sample_key = StubAttrsSimpleRecord.create_key()
    assert sample_key.get_key() == 'abc;123'

    # Create test record and populate with sample data
    context = rt.Context()
    record = StubAttrsSimpleRecord.create(context)

    # Test that context has been set
    assert record.context == context

    # Test primary key
    key = record.get_key()
    assert key == 'abc;123'

    # Test roundtrip serialization
    record_dict = record.to_dict()
    record_clone = StubAttrsSimpleRecord.from_dict(record_dict)
    record_clone_dict = record_clone.to_dict()
    assert len(record_dict) == 4
    assert record_dict == record_clone_dict


if __name__ == '__main__':
    pytest.main([__file__])
