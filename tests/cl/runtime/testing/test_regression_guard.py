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
    base_name = base_path.rsplit(".", 1)[-1]

    # Test 'output_path' from the test itself
    assert guard.output_path == base_path

    # Test 'output_path' inside an inner function
    channel = "test_function_channel"
    assert get_output_path_inside_function(channel) == f"{base_path}.{channel}"

    # Write output
    guard.write(f"Local guard: {base_name}")

    # Verify explicitly outside the 'with' clause
    guard.verify()

    for channel in ("with_channel.str", ("with_channel", "tuple")):
        with RegressionGuard(channel=channel) as context_guard:
            if isinstance(channel, tuple):
                channel = ".".join(channel)
            context_guard.write(f"{base_name}.{channel}.var")
            RegressionGuard.current().write(f"{base_name}.{channel}.current")
            RegressionGuard().write(f"{base_name}.{channel}.new")


class TestClass:
    """Stub pytest class."""

    def test_method(self):
        """Stub test method inside pytest class."""

        guard = RegressionGuard()
        base_path = f"{module_path}.test_class.test_method"
        base_name = ".".join(base_path.rsplit(".", 2)[-2:])

        # Test 'output_path' from the test itself
        assert guard.output_path == base_path

        # Test 'output_path' inside an inner function
        channel = "test_method_channel"
        assert get_output_path_inside_function(channel) == f"{base_path}.{channel}"

        guard.write(f"Local guard: {base_name}")
        guard.verify()

        # Check that verify_all will run verify on guards for which it is not called explicitly
        other_channel = "verify_all"
        other_guard = RegressionGuard(channel=other_channel)
        other_guard.write(f"{base_path}.{other_channel}")
        RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
