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
from cl.runtime.file.file_util import FileUtil


def test_check_valid_filename():
    """Test for 'check_valid_filename' method."""
    FileUtil.check_valid_filename("abc")  # Allow filenames without extension
    FileUtil.check_valid_filename("abc.xyz")
    with pytest.raises(RuntimeError):
        FileUtil.check_valid_filename("abc|xyz")
    with pytest.raises(RuntimeError):
        FileUtil.check_valid_filename("abc\\xyz")
    with pytest.raises(RuntimeError):
        FileUtil.check_valid_filename("abc/xyz")


def test_check_valid_path():
    """Test for 'check_valid_path' method."""
    FileUtil.check_valid_path("abc")  # Allow filenames without extension
    FileUtil.check_valid_path("abc.xyz")  # Allow filenames with no path
    FileUtil.check_valid_path("mydir\\mydir\\abc.xyz")
    FileUtil.check_valid_path("mydir/mydir/abc.xyz")
    with pytest.raises(RuntimeError):
        FileUtil.check_valid_filename("abc|xyz")
    with pytest.raises(RuntimeError):
        FileUtil.check_valid_filename("mydir\\mydir\\abc[xyz")


def test_has_extension():
    """Test for 'has_extension' method."""

    # Check for any extension
    assert FileUtil.has_extension("abc", None)
    assert not FileUtil.has_extension("abc.xyz", None)

    # Check for a specific extension
    assert FileUtil.has_extension("abc.xyz", "xyz")
    assert not FileUtil.has_extension("abc", "xyz")
    assert not FileUtil.has_extension("abc.xyz", "abc")


def test_check_extension():
    """Test for 'check_extension' method."""

    # Check for any extension
    FileUtil.check_extension("abc", None)
    with pytest.raises(RuntimeError):
        FileUtil.check_extension("abc.xyz", None)

    # Check for a specific extension
    FileUtil.check_extension("abc.xyz", "xyz")
    with pytest.raises(RuntimeError):
        FileUtil.check_extension("abc", "xyz")
    with pytest.raises(RuntimeError):
        FileUtil.check_extension("abc.xyz", "abc")


if __name__ == "__main__":
    pytest.main([__file__])
