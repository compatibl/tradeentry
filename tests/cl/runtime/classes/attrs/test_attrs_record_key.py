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
from stubs.cl.runtime.classes.attrs.stub_attrs_record_key import StubAttrsRecordKey


def test_smoke():
    """Smoke test."""

    # Create test base_record and populate with sample data
    key = StubAttrsRecordKey(str_field="abc", int_field=123)

    # Test type and key
    table_name = key.get_table()
    assert table_name == f"{type(key).__module__}.{type(key).__name__}"
    assert key.get_key() == "abc;123"

    # Test roundtrip serialization
    key_dict = key.to_dict()
    key_clone = StubAttrsRecordKey.from_dict(key_dict)
    key_clone_dict = key_clone.to_dict()
    assert len(key_dict) == 3
    assert key_dict == key_clone_dict


if __name__ == "__main__":
    pytest.main([__file__])
