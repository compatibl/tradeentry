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
from cl.runtime.testing.testing_util import TestingUtil


def test_get_test_name_in_function():
    """Test get_test_name in a test function."""
    assert TestingUtil.get_test_name() == "test_unit_test_util.test_get_test_name_in_function"


class TestClass:
    """Stub pytest class."""

    def test_get_test_name_in_method(self):
        """Test get_test_name in a test method."""
        assert TestingUtil.get_test_name() == "test_unit_test_util.test_class.test_get_test_name_in_method"


if __name__ == "__main__":
    pytest.main([__file__])
