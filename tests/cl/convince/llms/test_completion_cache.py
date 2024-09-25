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
import os
from typing import List
from cl.convince.llms.completion_cache import CompletionCache
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.testing.stack_util import StackUtil

module_path = __file__.removesuffix(".py")


def _delete_cache_files(base_dir: str, channels: List[str]):
    """Delete existing test cache files to prevent starting from previous test output or git diff at the end."""
    for channel in set(channels):
        if channel is not None and channel != "":
            filename = f"{channel}.completions.csv"
        else:
            filename = f"completions.csv"
        file_path = os.path.join(base_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)


def _get_request_id() -> str:
    """Get random request ID."""
    # Generate OrderedUuid and convert to readable ordered string in date-hash format
    request_uuid = OrderedUuid.create_one()
    request_id = OrderedUuid.to_readable_str(request_uuid)
    return request_id


def _perform_testing(base_dir: str):
    """Stub test function without a class."""

    # Test channels, the first two are repeated to test writing from two separate objects
    channels = ["channel.1", "channel.1", "channel.2"]

    # Delete the existing test cache files to prevent starting from previous test output
    _delete_cache_files(base_dir, channels)

    # Perform testing, two of the cache files are duplicates
    caches = [CompletionCache(channel=channel) for channel in channels]

    # Check that none are found before writing
    assert all(cache.get("a") is None for cache in caches)

    # Write a to all files
    [cache.add(_get_request_id(), "a", "b") for cache in caches]

    # Check that still none are found (because the cache files are not read after construction)
    assert all(cache.get("a") is None for cache in caches)

    # Recreate caches, this will reload files from disk
    caches = [CompletionCache(channel=channel) for channel in channels]

    # Make sure "a" is found for all caches
    assert all(cache.get("a") == "b" for cache in caches)

    # Check that e is found in none
    assert all(cache.get("e") is None for cache in caches)

    # Write c to the first file only
    caches[0].add(_get_request_id(), "c", "d")

    # Check that c is not found (because the cache files are not read after construction)
    assert caches[0].get("c") is None
    assert caches[1].get("c") is None
    assert caches[2].get("c") is None

    # Recreate caches, this will reload files from disk
    caches = [CompletionCache(channel=channel) for channel in channels]

    # Reload and confirm it is visible to the first two now
    assert caches[0].get("c") == "d"
    assert caches[1].get("c") == "d"
    assert caches[2].get("c") is None

    # Write another value for "a", the file should have both but the new value is returned by get
    caches[0].add(_get_request_id(), "a", "bb")

    # Recreate caches, this will reload files from disk
    caches = [CompletionCache(channel=channel) for channel in channels]

    # Check for new values
    assert caches[0].get("a") == "bb"
    assert caches[1].get("a") == "bb"
    assert caches[2].get("a") == "b"

    # Delete the generated test cache files to prevent git diff
    _delete_cache_files(base_dir, channels)


def test_function():
    """Stub test function without a class."""

    # Test calling from a function
    base_dir = StackUtil.get_base_dir()
    _perform_testing(base_dir)


class TestClass:
    """Stub pytest class."""

    def test_method(self):
        """Stub test method inside pytest class."""

        # Test calling from a method
        base_dir = StackUtil.get_base_dir()
        _perform_testing(base_dir)


if __name__ == "__main__":
    pytest.main([__file__])
