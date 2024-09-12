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
from cl.runtime.testing.pytest_util import PytestUtil


def test_is_inside_pytest():
    """Test get_caller_name method."""
    assert PytestUtil.is_inside_pytest() is True


def test_get_current_pytest():
    """Test get_caller_name method."""

    assert PytestUtil.get_current_pytest()  # TODO: Add assert for the result to the test


def test_get_caller_name():
    """Test get_caller_name method."""

    assert PytestUtil.get_caller_name(caller_file=__file__) == "test_pytest_util"


if __name__ == "__main__":
    pytest.main([__file__])
