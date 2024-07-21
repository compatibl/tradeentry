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
from cl.runtime.testing.regression_guard import RegressionGuard

module_path = __file__.removesuffix(".py")


def get_output_path_inside_function(channel: str) -> str:
    """Stub function invoked from the test."""
    channel_guard = RegressionGuard(channel=channel)
    channel_guard.write(f"Channel guard: {channel}")
    channel_guard.verify()
    return channel_guard.output_path


def get_output_path_for_current_guard(channel: str | None = None) -> str:
    """Stub function invoked from the test."""
    current_guard = RegressionGuard.current()
    if channel is not None:
        current_guard.write(f"Current guard with channel: {channel}")
    else:
        current_guard.write("Current guard")
    return current_guard.output_path


def test_function():
    """Stub test function without a class."""

    guard = RegressionGuard()
    base_path = f"{module_path}.test_function"

    # Test 'output_path' from the test itself
    assert guard.output_path == base_path

    # Test 'output_path' inside an inner function
    channel = "test_function_channel"
    assert get_output_path_inside_function(channel) == f"{base_path}.{channel}"

    # Write output
    guard.write("Local guard: test_function")
    guard.verify()


class TestClass:
    """Stub pytest class."""

    def test_method(self):
        """Stub test method inside pytest class."""

        guard = RegressionGuard()
        base_path = f"{module_path}.test_class.test_method"

        # Test 'output_path' from the test itself
        assert guard.output_path == base_path

        # Test 'output_path' inside an inner function
        channel = "test_method_channel"
        assert get_output_path_inside_function(channel) == f"{base_path}.{channel}"

        guard.write("Local guard: test_method")
        guard.verify()


if __name__ == "__main__":
    pytest.main([__file__])
