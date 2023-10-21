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
from stubs.runtime.storage.stub_data import StubData

# Tests for Data


def test_smoke():
    """Smoke test."""

    # Create test record and populate with sample data
    obj = StubData.create()

    # Test roundtrip serialization
    data1 = obj.to_dict()
    obj2 = StubData()
    obj2.from_dict(data1)
    data2 = obj2.to_dict()
    assert len(data2.keys()) == 2
    assert data1 == data2


if __name__ == '__main__':
    pytest.main([__file__])
