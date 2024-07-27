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


def perform_testing(base_path: str):
    """Stub test function without a class."""

    base_name = base_path.rsplit(".", 1)[-1]

    # Guard without channel
    guard_without_channel = RegressionGuard()
    assert guard_without_channel.output_path == base_path

    # Write output
    guard_without_channel.write(base_name)

    # Verify single guard
    guard_without_channel.verify()

    for channel in ("with_channel.str", ("with_channel", "tuple")):
        # First instance of guard, created using tuple or string
        guard_with_channel_1 = RegressionGuard(channel=channel)
        channel_str = ".".join(channel) if isinstance(channel, tuple) else channel
        guard_with_channel_1.write(f"{base_name}.{channel_str}.1")

        # Second instance of guard for the same channel, created using string
        guard_with_channel_2 = RegressionGuard(channel=channel_str)
        guard_with_channel_2.write(f"{base_name}.{channel_str}.2")

    # Verify all guards
    RegressionGuard.verify_all()

    # Verify again, should have no effect
    RegressionGuard.verify_all()


def test_function():
    """Stub test function without a class."""

    # Test calling regression guard from a function
    perform_testing(f"{module_path}.test_function")


class TestClass:
    """Stub pytest class."""

    def test_method(self):
        """Stub test method inside pytest class."""

        # Test calling regression guard from a method
        perform_testing(f"{module_path}.test_class.test_method")


if __name__ == "__main__":
    pytest.main([__file__])
