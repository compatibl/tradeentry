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
from stubs.cl.runtime import StubIntEnum


def test_smoke():
    """Smoke test."""

    assert StubIntEnum.ENUM_VALUE_1 == 1


def test_class_label():
    """Rename test."""

    # TODO: Add test for renamed enum class label


def test_item_label():
    """Rename test."""

    # TODO: Add test for renamed enum item label


if __name__ == '__main__':
    pytest.main([__file__])
