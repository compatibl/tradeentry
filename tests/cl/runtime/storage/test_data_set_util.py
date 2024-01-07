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
from cl.runtime.storage.data_set_util import DataSetUtil


def test_to_tokens():
    """Test conversion of dataset string to tokens."""

    assert DataSetUtil.to_tokens("/") == []
    assert DataSetUtil.to_tokens("/A") == ["A"]
    assert DataSetUtil.to_tokens("/A/B") == ["A", "B"]

    with pytest.raises(Exception):
        DataSetUtil.to_tokens("")
    with pytest.raises(Exception):
        DataSetUtil.to_tokens(" ")
    with pytest.raises(Exception):
        DataSetUtil.to_tokens(" A")
    with pytest.raises(Exception):
        DataSetUtil.to_tokens("A ")
    with pytest.raises(Exception):
        DataSetUtil.to_tokens("A")
    with pytest.raises(Exception):
        DataSetUtil.to_tokens("/A/")
    with pytest.raises(Exception):
        DataSetUtil.to_tokens("/ A")
    with pytest.raises(Exception):
        DataSetUtil.to_tokens("/A /B")


def test_from_tokens():
    """Test conversion of a list of tokens to dataset string."""

    assert DataSetUtil.from_tokens([]) == "/"
    assert DataSetUtil.from_tokens(["A"]) == "/A"
    assert DataSetUtil.from_tokens(["A", "B"]) == "/A/B"

    with pytest.raises(Exception):
        DataSetUtil.from_tokens(["/"])
    with pytest.raises(Exception):
        DataSetUtil.from_tokens([" "])
    with pytest.raises(Exception):
        DataSetUtil.from_tokens([" A"])
    with pytest.raises(Exception):
        DataSetUtil.from_tokens(["A "])


if __name__ == '__main__':
    pytest.main([__file__])
