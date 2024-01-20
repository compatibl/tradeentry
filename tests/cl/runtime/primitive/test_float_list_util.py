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
from cl.runtime.primitive.float_list_util import FloatListUtil
from stubs.cl.runtime.primitive.stub_float_util import StubFloatUtil


def test_is_strictly_ascending():
    """Test is_strictly_ascending method."""
    assert FloatListUtil.is_strictly_ascending(StubFloatUtil.create_strictly_ascending_list())
    assert not FloatListUtil.is_strictly_ascending(StubFloatUtil.create_equal_or_ascending_list())
    assert not FloatListUtil.is_strictly_ascending(StubFloatUtil.create_equal_or_ascending_list_with_tolerance())
    assert not FloatListUtil.is_strictly_ascending(StubFloatUtil.create_strictly_descending_list())
    assert not FloatListUtil.is_strictly_ascending(StubFloatUtil.create_equal_or_descending_list())
    assert not FloatListUtil.is_strictly_ascending(StubFloatUtil.create_equal_or_descending_list_with_tolerance())


def test_is_equal_or_ascending():
    """Test is_equal_or_ascending method."""
    assert FloatListUtil.is_equal_or_ascending(StubFloatUtil.create_strictly_ascending_list())
    assert FloatListUtil.is_equal_or_ascending(StubFloatUtil.create_equal_or_ascending_list())
    assert FloatListUtil.is_equal_or_ascending(StubFloatUtil.create_equal_or_ascending_list_with_tolerance())
    assert not FloatListUtil.is_equal_or_ascending(StubFloatUtil.create_strictly_descending_list())
    assert not FloatListUtil.is_equal_or_ascending(StubFloatUtil.create_equal_or_descending_list())
    assert not FloatListUtil.is_equal_or_ascending(StubFloatUtil.create_equal_or_descending_list_with_tolerance())


def test_is_strictly_descending():
    """Test is_strictly_descending method."""
    assert not FloatListUtil.is_strictly_descending(StubFloatUtil.create_strictly_ascending_list())
    assert not FloatListUtil.is_strictly_descending(StubFloatUtil.create_equal_or_ascending_list())
    assert not FloatListUtil.is_strictly_descending(StubFloatUtil.create_equal_or_ascending_list_with_tolerance())
    assert FloatListUtil.is_strictly_descending(StubFloatUtil.create_strictly_descending_list())
    assert not FloatListUtil.is_strictly_descending(StubFloatUtil.create_equal_or_descending_list())
    assert not FloatListUtil.is_strictly_descending(StubFloatUtil.create_equal_or_descending_list_with_tolerance())


def test_is_equal_or_descending():
    """Test is_equal_or_descending method."""
    assert not FloatListUtil.is_equal_or_descending(StubFloatUtil.create_strictly_ascending_list())
    assert not FloatListUtil.is_equal_or_descending(StubFloatUtil.create_equal_or_ascending_list())
    assert not FloatListUtil.is_equal_or_descending(StubFloatUtil.create_equal_or_ascending_list_with_tolerance())
    assert FloatListUtil.is_equal_or_descending(StubFloatUtil.create_strictly_descending_list())
    assert FloatListUtil.is_equal_or_descending(StubFloatUtil.create_equal_or_descending_list())
    assert FloatListUtil.is_equal_or_descending(StubFloatUtil.create_equal_or_descending_list_with_tolerance())


if __name__ == '__main__':
    pytest.main([__file__])
