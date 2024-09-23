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
from cl.convince.llms.completion_cache import CompletionCache

module_path = __file__.removesuffix(".py")


def perform_testing(base_path: str, full: bool = False):
    """Stub test function without a class."""

    # Test channels, the first two are repeated to test writing from two separate objects
    channels = ["channel.1", "channel.1", "channel.2"]

    # Delete existing test cache files to prevent starting from previous test output
    for unique_channel in set(channels):
        file_path = f"{base_path}.{unique_channel}.completions.csv"
        if os.path.exists(file_path):
            os.remove(file_path)

    # Perform testing
    caches = [CompletionCache(channel=channel) for channel in channels]
    assert all(cache.lookup("a") is None for cache in caches)
    [cache.write("a", "b") for cache in caches]
    x = [cache.lookup("a") == "b" for cache in caches]
    # x = caches[0].lookup("a")
    pass


def test_function():
    """Stub test function without a class."""

    # Test calling regression guard from a function
    perform_testing(f"{module_path}.test_function", full=True)


class TestClass:
    """Stub pytest class."""

    def test_method(self):
        """Stub test method inside pytest class."""

        # Test calling regression guard from a method
        perform_testing(f"{module_path}.test_class.test_method")


if __name__ == "__main__":
    pytest.main([__file__])
