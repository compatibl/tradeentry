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


def get_output_path_inside_function(channel: str) -> str:
    """Stub function invoked from the test."""
    channel_guard = RegressionGuard(channel=channel)
    channel_guard.write(channel)
    return channel_guard.output_path


def test_stub_function():
    """Stub test function without a class."""

    guard = RegressionGuard()

    # Test 'output_path' from the test itself
    assert guard.output_path == f"{module_path}.test_stub_function"

    # Test 'output_path' inside an inner function
    channel = "channel_1"
    assert get_output_path_inside_function(channel) == f"{module_path}.test_stub_function.{channel}"

    # Write output
    guard.write("text")
    guard.verify()


class TestStubPytest:
    """Stub pytest class."""

    def test_stub_method(self):
        """Stub test method inside pytest class."""

        # Test 'output_path' from the test itself
        assert RegressionGuard().output_path == f"{module_path}.test_stub_pytest.test_stub_method"

        # Test 'output_path' inside an inner function
        channel = "channel_2"
        assert get_output_path_inside_function(channel) == f"{module_path}.test_stub_pytest.test_stub_method.{channel}"


class TestStubUnittest(unittest.TestCase):
    """Stub unittest class."""

    def test_unittest_method(self):
        """Stub test method inside unittest class."""

        # Test 'output_path' from the test itself
        assert RegressionGuard().output_path == f"{module_path}.test_stub_unittest.test_unittest_method"

        # Test 'output_path' inside an inner function
        channel = "channel_3"
        assert get_output_path_inside_function(channel) == f"{module_path}.test_stub_unittest.test_unittest_method.{channel}"


if __name__ == "__main__":

    # Run pytest tests
    pytest.main([__file__])

    # Run unittest tests
    unittest.main()
