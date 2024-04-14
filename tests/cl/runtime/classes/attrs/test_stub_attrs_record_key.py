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

import copy
import pytest
from stubs.cl.runtime.classes.attrs.stub_attrs_nested_fields_key import StubAttrsNestedFieldsKey
from stubs.cl.runtime.classes.attrs.stub_attrs_record_key import StubAttrsRecordKey


def test_smoke():
    """Smoke test."""

    key_1 = StubAttrsRecordKey(str_field="A", int_field=0)
    key_2 = StubAttrsRecordKey(str_field="B", int_field=0)

    assert "A;0" == StubAttrsRecordKey.to_str_key(StubAttrsRecordKey, key_1)
    assert "B;0" == StubAttrsRecordKey.to_str_key(StubAttrsRecordKey, key_2)


def test_composite_key():
    """Test composite key where key some elements are also keys."""

    key_1 = StubAttrsRecordKey(str_field="A", int_field=0)
    key_same_as_1 = StubAttrsRecordKey(str_field="A", int_field=0)
    key_2 = StubAttrsRecordKey(str_field="B", int_field=1)

    composite_key_1 = StubAttrsNestedFieldsKey(primitive="A", embedded_1=key_1, embedded_2=key_2)
    composite_key_1_prime = StubAttrsNestedFieldsKey(primitive="A", embedded_1=key_same_as_1, embedded_2=key_2)
    composite_key_2 = StubAttrsNestedFieldsKey(primitive="B", embedded_1=key_1, embedded_2=key_2)

    assert "A;A;0;B;1" == str(composite_key_1)
    assert "B;A;0;B;1" == str(composite_key_2)

    assert composite_key_1 == composite_key_1_prime
    assert composite_key_1 != composite_key_2


def test_comparison():
    """Test comparison"""

    key_1 = StubAttrsRecordKey(str_field="A", int_field=0)
    key_2 = StubAttrsRecordKey(str_field="B", int_field=1)
    key_1_copy = copy.deepcopy(key_1)

    assert key_1 == key_1_copy
    assert key_1 != key_2


if __name__ == "__main__":
    pytest.main([__file__])
