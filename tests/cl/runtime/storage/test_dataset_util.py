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


def test_to_tokens():
    """Test conversion of dataset string to tokens."""

    assert DatasetUtil.to_tokens(None) == []
    assert DatasetUtil.to_tokens("") == []
    assert DatasetUtil.to_tokens("A") == ["A"]
    assert DatasetUtil.to_tokens("A\\B") == ["A", "B"]

    with pytest.raises(Exception):
        assert DatasetUtil.to_tokens(" ")
    with pytest.raises(Exception):
        assert DatasetUtil.to_tokens(" A")
    with pytest.raises(Exception):
        assert DatasetUtil.to_tokens("A ")
    with pytest.raises(Exception):
        assert DatasetUtil.to_tokens(" A\\B")
    with pytest.raises(Exception):
        assert DatasetUtil.to_tokens("A\\B ")
    with pytest.raises(Exception):
        assert DatasetUtil.to_tokens("A \\B")
    with pytest.raises(Exception):
        assert DatasetUtil.to_tokens("A\\ B")
    with pytest.raises(Exception):
        DatasetUtil.to_tokens("\\A")
    with pytest.raises(Exception):
        DatasetUtil.to_tokens("A\\")
    with pytest.raises(Exception):
        DatasetUtil.to_tokens("\\A\\")
    with pytest.raises(Exception):
        DatasetUtil.to_tokens("\\ A")
    with pytest.raises(Exception):
        DatasetUtil.to_tokens("\\A \\B")


def test_combine():
    """Test method combine(...)"""

    assert DatasetUtil.combine() is None
    assert DatasetUtil.combine(None) is None
    assert DatasetUtil.combine("") is None
    assert DatasetUtil.combine("A") == "A"
    assert DatasetUtil.combine("A", "B") == "A\\B"
    assert DatasetUtil.combine(None, "A", "B") == "A\\B"

    with pytest.raises(Exception):
        DatasetUtil.combine("\\")
    with pytest.raises(Exception):
        DatasetUtil.combine(" ")
    with pytest.raises(Exception):
        DatasetUtil.combine(" A")
    with pytest.raises(Exception):
        DatasetUtil.combine("A ")
    with pytest.raises(Exception):
        DatasetUtil.combine("\\A", "B")
    with pytest.raises(Exception):
        DatasetUtil.combine("A", "B\\")
    with pytest.raises(Exception):
        DatasetUtil.combine("A", "\\B")
    with pytest.raises(Exception):
        DatasetUtil.combine("A\\", "B")


if __name__ == "__main__":
    pytest.main([__file__])
