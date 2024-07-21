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
import unittest

from cl.runtime.testing.regression_guard import RegressionGuard

module_path = __file__.removesuffix(".py")


def get_output_path_inside_function() -> str:
    """Stub function invoked from the test."""
    return RegressionGuard().output_path


def test_stub_function():
    """Stub test function without a class."""

    # Test calling 'get_output_path' from the test itself
    result = RegressionGuard().output_path
    assert result == f"{module_path}.test_stub_function"

    # Test calling 'get_output_path' inside an inner function
    assert get_output_path_inside_function() == result


class TestStubPytest:
    """Stub pytest class."""

    def test_stub_method(self):
        """Stub test method inside pytest class."""

        # Test calling 'get_output_path' from the test itself
        result = RegressionGuard().output_path
        assert result == f"{module_path}.test_stub_pytest.test_stub_method"

        # Test calling 'get_output_path' inside an inner function
        assert get_output_path_inside_function() == result


class TestStubUnittest(unittest.TestCase):
    """Stub unittest class."""

    def test_unittest_method(self):
        """Stub test method inside unittest class."""

        # Test calling 'get_output_path' from the test itself
        result = RegressionGuard().output_path
        assert result == f"{module_path}.test_stub_unittest.test_unittest_method"

        # Test calling 'get_output_path' inside an inner function
        assert get_output_path_inside_function() == result


if __name__ == "__main__":

    # Run pytest tests
    pytest.main([__file__])

    # Run unittest tests
    unittest.main()
