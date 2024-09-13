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
from cl.runtime.testing.pytest_fixtures import local_dir_fixture


def _normalize_path(path: str) -> str:
    """Normalize path to a standard form for comparison."""
    # Expand user directory (e.g., ~/ on Unix-like systems)
    path = os.path.expanduser(path)
    # Resolve any symbolic links and normalize the path
    path = os.path.realpath(path)
    # Convert to absolute path
    path = os.path.abspath(path)
    return path


def test_local_dir_fixture(local_dir_fixture):
    """Test that local_dir_fixture makes current working directory the same as the test directory."""

    # Get directories
    current_dir = os.getcwd()  # Current working directory
    test_dir = os.path.dirname(os.path.abspath(__file__))  # Directory where this test is located

    # Normalize for comparison and compare
    current_dir = _normalize_path(current_dir)
    test_dir = _normalize_path(test_dir)
    assert current_dir == test_dir


if __name__ == "__main__":
    pytest.main([__file__])
