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
import os

import pytest
from cl.runtime.testing.regression_guard import RegressionGuard

module_path = __file__.removesuffix(".py")


def perform_testing(base_path: str, full: bool = False):
    """Stub test function without a class."""

    test_str = "perform_testing"

    # Guard without channel
    guard_without_channel = RegressionGuard()
    assert guard_without_channel.output_path == base_path

    # Write output
    guard_without_channel.write(test_str)

    # Verify single guard
    guard_without_channel.verify()

    # Run additional tests only if full testing is specified
    if full:
        # Test channels
        guard_with_channel_1 = RegressionGuard(channel="channel")
        guard_with_channel_1.write(f"{test_str}.1")

        # Second instance of guard for the same channel, created using string
        guard_with_channel_2 = RegressionGuard(channel="channel")
        guard_with_channel_2.write(f"{test_str}.2")

        # Test dict output
        test_dict = {
            "str_key": "abc",
            "int_key": 1,
            "float_key": 1.23,
            "bool_key": True,
            "dict_key": {
                "nested_str_key": "def",
                "nested_int_key": 2,
            },
            "str_list_key": ["abc", "def"],
            "int_list_key": [1, 2],
        }
        RegressionGuard(channel="dict_txt").write(test_dict)

        # Verify all guards
        RegressionGuard.verify_all()

        # Verify again, should have no effect
        RegressionGuard.verify_all()


def test_function():
    """Stub test function without a class."""

    # Test calling regression guard from a function
    expected_path = os.path.join(module_path, "test_function")
    perform_testing(expected_path, full=True)


class TestClass:
    """Stub pytest class."""

    def test_method(self):
        """Stub test method inside pytest class."""

        # Test calling regression guard from a method
        expected_path = os.path.join(module_path, "test_class", "test_method")
        perform_testing(expected_path, full=True)


if __name__ == "__main__":
    pytest.main([__file__])
