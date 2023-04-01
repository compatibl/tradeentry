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
import tests

# Tests for Record


def test_smoke():
    """Smoke test."""

    # Create test record and populate with sample data
    context = rt.Context()
    record = tests.MockRecord.create(context)

    # Test that context has been set
    assert record.context == context

    # Test primary key
    pk = record.to_pk()
    assert pk == 'samples.RecordSample;abc;123'

    # Test roundtrip serialization
    data1 = record.to_dict()
    record2 = tests.MockRecord()
    record2.context = context
    record2.from_dict(data1)
    data2 = record2.to_dict()
    assert len(data2.keys()) == 4
    assert data1 == data2


if __name__ == '__main__':
    pytest.main([__file__])
