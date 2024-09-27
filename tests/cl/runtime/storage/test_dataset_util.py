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
from cl.runtime.storage.dataset_util import DatasetUtil


def test_to_levels():
    """Test conversion of dataset string to levels."""

    assert DatasetUtil.to_levels(None) == []
    assert DatasetUtil.to_levels("\\") == []
    assert DatasetUtil.to_levels("\\abc") == ["abc"]
    assert DatasetUtil.to_levels("\\abc\\def") == ["abc", "def"]

    with pytest.raises(Exception):
        assert DatasetUtil.to_levels(" ")
    with pytest.raises(Exception):
        assert DatasetUtil.to_levels(" abc")
    with pytest.raises(Exception):
        assert DatasetUtil.to_levels("abc ")
    with pytest.raises(Exception):
        assert DatasetUtil.to_levels(" abc\\def")
    with pytest.raises(Exception):
        assert DatasetUtil.to_levels("\\abc\\def ")
    with pytest.raises(Exception):
        assert DatasetUtil.to_levels("\\abc \\def")
    with pytest.raises(Exception):
        assert DatasetUtil.to_levels("\\abc\\ def")
    with pytest.raises(Exception):
        DatasetUtil.to_levels("\\abc\\")
    with pytest.raises(Exception):
        DatasetUtil.to_levels("\\abc\\")
    with pytest.raises(Exception):
        DatasetUtil.to_levels("\\ abc")
    with pytest.raises(Exception):
        DatasetUtil.to_levels("\\abc \\def")


def test_combine():
    """Test DatasetUtil.combine."""

    assert DatasetUtil.combine(None) == "\\"
    assert DatasetUtil.combine("\\") == "\\"
    assert DatasetUtil.combine(None, None) == "\\"
    assert DatasetUtil.combine("\\", None) == "\\"
    assert DatasetUtil.combine(None, "\\abc") == "\\abc"
    assert DatasetUtil.combine("\\abc", None) == "\\abc"
    assert DatasetUtil.combine("abc") == "\\abc"
    assert DatasetUtil.combine("abc", "def") == "\\abc\\def"
    assert DatasetUtil.combine(None, "abc", "def") == "\\abc\\def"
    assert DatasetUtil.combine("abc", None, "def") == "\\abc\\def"
    assert DatasetUtil.combine("\\abc") == "\\abc"
    assert DatasetUtil.combine("\\abc\\def") == "\\abc\\def"
    assert DatasetUtil.combine("\\abc", "\\def") == "\\abc\\def"
    assert DatasetUtil.combine(None, "abc", "def") == "\\abc\\def"

    with pytest.raises(Exception):
        DatasetUtil.combine("\\\\")
    with pytest.raises(Exception):
        DatasetUtil.combine(" ")
    with pytest.raises(Exception):
        DatasetUtil.combine(" abc")
    with pytest.raises(Exception):
        DatasetUtil.combine("abc ")
    with pytest.raises(Exception):
        DatasetUtil.combine("abc", "def\\")
    with pytest.raises(Exception):
        DatasetUtil.combine("abc\\", "def")


def test_lookup_list():
    """Test DatasetUtil.to_lookup_list."""

    assert DatasetUtil.to_lookup_list(None) == ["\\"]
    assert DatasetUtil.to_lookup_list("\\") == ["\\"]
    assert DatasetUtil.to_lookup_list("\\abc") == ["\\abc", "\\"]
    assert DatasetUtil.to_lookup_list("\\abc\\def") == ["\\abc\\def", "\\abc", "\\"]


if __name__ == "__main__":
    pytest.main([__file__])
