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


def test_pascal_to_snake_case():
    """Test for case conversion from PascalCase to snake_case."""

    # From snake_case without dot delimiter
    assert StringUtil.pascal_to_snake_case("AbcDef") == "abc_def"
    assert StringUtil.pascal_to_snake_case("Some2dPoint") == "some2d_point"  # TODO: Should be an input format error
    assert StringUtil.pascal_to_snake_case("Great2DPicture") == "great2d_picture"

    # From snake_case with dot delimiter
    assert StringUtil.pascal_to_snake_case("Abc.Def") == "abc.def"
    assert StringUtil.pascal_to_snake_case("AbcDef.Xyz") == "abc_def.xyz"
    assert StringUtil.pascal_to_snake_case("AbcDef.UvwXyz") == "abc_def.uvw_xyz"


def test_upper_to_snake_case():
    """Test for case conversion from UPPER_CASE to snake_case."""

    # From UPPER_CASE without dot delimiter
    assert StringUtil.upper_to_snake_case("ABC_DEF") == "abc_def"

    # From UPPER_CASE with dot delimiter
    assert StringUtil.upper_to_snake_case("ABC_DEF.XYZ") == "abc_def.xyz"


def test_snake_to_pascal_case():
    """Test for case conversion from snake_case to PascalCase."""

    # From snake_case without dot delimiter
    assert StringUtil.snake_to_pascal_case("abc_def") == "AbcDef"
    assert StringUtil.snake_to_pascal_case("some2d_point") == "Some2dPoint"
    assert StringUtil.snake_to_pascal_case("great2_d_picture") == "Great2DPicture"

    # From snake_case with dot delimiter
    assert StringUtil.snake_to_pascal_case("abc.def") == "Abc.Def"
    assert StringUtil.snake_to_pascal_case("abc_def.xyz") == "AbcDef.Xyz"
    assert StringUtil.snake_to_pascal_case("abc_def.uvw_xyz") == "AbcDef.UvwXyz"


def test_upper_to_pascal_case():
    """Test for case conversion from UPPER_CASE to PascalCase."""

    # From UPPER_CASE without dot delimiter
    assert StringUtil.upper_to_pascal_case("ABC_DEF") == "AbcDef"

    # From UPPER_CASE with dot delimiter
    assert StringUtil.upper_to_pascal_case("ABC_DEF.XYZ") == "AbcDef.Xyz"


def test_pascal_to_upper_case():
    """Test for case conversion from PascalCase to UPPER_CASE."""

    # From UPPER_CASE without dot delimiter
    assert StringUtil.pascal_to_upper_case("AbcDef") == "ABC_DEF"

    # From UPPER_CASE with dot delimiter
    assert StringUtil.pascal_to_upper_case("AbcDef.Xyz") == "ABC_DEF.XYZ"


if __name__ == "__main__":
    pytest.main([__file__])
