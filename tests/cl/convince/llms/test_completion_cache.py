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

    # Perform testing, two of the cache files are duplicates
    caches = [CompletionCache(channel=channel) for channel in channels]

    # Check that none are found befoe writing
    assert all(cache.get("a") is None for cache in caches)

    # Write a to all files
    [cache.add("a", "b") for cache in caches]

    # Check that all is found in all
    assert all(cache.get("a") == "b" for cache in caches)

    # Check that e is found in none
    assert all(cache.get("e") is None for cache in caches)

    # Write c to the first file only
    caches[0].add("c", "d")

    # Check that c is found only in the first one before reload (because the cache file is not read during the run)
    assert caches[0].get("c") == "d"
    assert caches[1].get("c") is None
    assert caches[2].get("c") is None

    # Reload and confirm it is visible to the first two now
    caches = [CompletionCache(channel=channel) for channel in channels]
    assert caches[0].get("c") == "d"
    assert caches[1].get("c") == "d"
    assert caches[2].get("c") is None

    # Write another value for "a", the file should have both but the new value is returned by get
    caches[0].add("a", "bb")
    caches = [CompletionCache(channel=channel) for channel in channels]
    assert caches[0].get("a") == "bb"
    assert caches[1].get("a") == "bb"
    assert caches[2].get("a") == "b"


def test_function():
    """Stub test function without a class."""

    # Test calling from a function
    perform_testing(f"{module_path}.test_function", full=True)


class TestClass:
    """Stub pytest class."""

    def test_method(self):
        """Stub test method inside pytest class."""

        # Test calling from a method
        perform_testing(f"{module_path}.test_class.test_method")


if __name__ == "__main__":
    pytest.main([__file__])
