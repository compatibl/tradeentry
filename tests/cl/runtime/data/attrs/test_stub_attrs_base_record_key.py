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
import copy
from stubs.cl.runtime.data.attrs.stub_attrs_composite_key import StubAttrsCompositeKey
from stubs.cl.runtime.data.attrs.stub_attrs_record_key import StubAttrsRecordKey


def test_smoke():
    """Smoke test."""

    key_a0 = StubAttrsRecordKey(record_id='A', record_index=0)
    key_b0 = StubAttrsRecordKey(record_id='B', record_index=0)

    assert 'A;0' == str(key_a0)
    assert 'B;0' == str(key_b0)


def test_composite_key():
    """Test composite key where key some elements are also keys."""

    base_key_1 = StubAttrsRecordKey(record_id='A', record_index=0)
    base_key_same_as_1 = StubAttrsRecordKey(record_id='A', record_index=0)
    base_key_2 = StubAttrsRecordKey(record_id='B', record_index=1)

    composite_key_1 = StubAttrsCompositeKey(str_key_0='A', embedded_key_1=base_key_1, embedded_key_2=base_key_2)
    composite_key_same_as_1 = StubAttrsCompositeKey(
        str_key_0='A', embedded_key_1=base_key_same_as_1, embedded_key_2=base_key_2
    )
    composite_key_2 = StubAttrsCompositeKey(str_key_0='B', embedded_key_1=base_key_1, embedded_key_2=base_key_2)

    assert 'A;A;0;B;1' == str(composite_key_1)
    assert 'B;A;0;B;1' == str(composite_key_2)

    assert composite_key_1 == composite_key_same_as_1
    assert composite_key_1 != composite_key_2


def test_comparison():
    """Test comparison"""

    base_key_1 = StubAttrsRecordKey(record_id='A', record_index=0)
    base_key_2 = StubAttrsRecordKey(record_id='B', record_index=1)
    base_key_1_copy = copy.deepcopy(base_key_1)

    assert base_key_1 == base_key_1_copy
    assert base_key_1 != base_key_2


if __name__ == '__main__':
    pytest.main([__file__])
