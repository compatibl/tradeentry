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
from cl.runtime.primitive.char_util import _FLAGGED_CHARS
from cl.runtime.primitive.char_util import _REMOVED_CHARS
from cl.runtime.primitive.char_util import _REPLACED_CHARS
from cl.runtime.primitive.char_util import CharUtil
from cl.runtime.testing.regression_guard import RegressionGuard


def test_normalize_text():
    """Test CharUtil.normalize_text."""

    guard = RegressionGuard()
    guard.write(CharUtil.normalize_chars(f"{','.join(_REMOVED_CHARS)}"))
    guard.write(CharUtil.normalize_chars(f"{','.join(_REPLACED_CHARS)}"))
    RegressionGuard.verify_all()

    for char in _FLAGGED_CHARS:
        with pytest.raises(Exception):
            CharUtil.normalize_chars(f"abc{char}def")


def test_describe_char():
    """Test CharUtil.describe_char."""
    assert CharUtil.describe_char("\n") == "Newline"
    assert CharUtil.describe_char("\r") == "Carriage Return"
    assert CharUtil.describe_char("\ufeff") == "UTF-8 BOM"


if __name__ == "__main__":
    pytest.main([__file__])
