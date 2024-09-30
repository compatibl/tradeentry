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
from cl.runtime.primitive.string_util import StringUtil


def test_is_empty():
    """Smoke test for functions in StringUtil."""
    assert StringUtil.is_empty(None)
    assert StringUtil.is_empty("")
    assert not StringUtil.is_empty("abc")

def test_to_pascal_case():
    """Smoke test for functions in StringUtil."""

    # Without dot delimiter
    assert StringUtil.to_pascal_case("abc_def") == "AbcDef"
    assert StringUtil.to_pascal_case("some2d_point") == "Some2dPoint"
    assert StringUtil.to_pascal_case("great2_d_picture") == "Great2DPicture"

    # With dot delimiter
    assert StringUtil.to_pascal_case("abc.def") == "Abc.Def"
    assert StringUtil.to_pascal_case("abc_def.uvw_xyz") == "AbcDef.UvwXyz"


def test_to_snake_case():
    """Smoke test for functions in StringUtil."""

    # Without dot delimiter
    assert StringUtil.to_snake_case("AbcDef") == "abc_def"
    assert StringUtil.to_snake_case("Some2dPoint") == "some2d_point"
    assert StringUtil.to_snake_case("Great2DPicture") == "great2d_picture"

    # With dot delimiter
    assert StringUtil.to_snake_case("Abc.Def") == "abc.def"
    assert StringUtil.to_snake_case("AbcDef.UvwXyz") == "abc_def.uvw_xyz"


if __name__ == "__main__":
    pytest.main([__file__])
