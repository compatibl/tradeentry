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
from cl.runtime.primitive.float_util import FloatUtil


def test_format():
    """Test conversion of float to string."""

    assert FloatUtil.format(1000.0) == "1000."
    assert FloatUtil.format(-1000.0) == "-1000."
    assert FloatUtil.format(0) == "0."
    assert FloatUtil.format(0.01) == "0.01"
    assert FloatUtil.format(-0.01) == "-0.01"
    assert FloatUtil.format(1000.0000000000000000000000123) == "1000."
    assert FloatUtil.format(1000.000123000000000000000000123) == "1000.000123"
    assert FloatUtil.format(1000.112233445566778899) == "1000.1122334456"
    assert FloatUtil.format(0.000112233445566778899) == "0.0001122334"
    assert (
        FloatUtil.format(1000000000000000000000000.000123000000000000000000123) == "1000000000000000000000000."
    )  # Float precision not enough for the fractional part .000123
    assert (
        FloatUtil.format(-1000000000000000000000000.000123000000000000000000123) == "-1000000000000000000000000."
    )  # Float precision not enough for the fractional part .000123
    assert FloatUtil.format(0.000000000000000000000000123) == "0."


def test_get_int():
    """Test get_int method."""

    assert FloatUtil.get_int(value=1.0) == 1
    assert FloatUtil.get_int(value=-1.0) == -1
    with pytest.raises(RuntimeError):
        assert FloatUtil.get_int(value=0.5) == 1


if __name__ == "__main__":
    pytest.main([__file__])
