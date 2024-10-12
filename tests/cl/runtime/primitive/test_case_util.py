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
from cl.runtime.primitive.case_util import CaseUtil


def check_raises_error(check_function, value, expected_message):
    with pytest.raises(RuntimeError) as exc_info:
        check_function(value)
    assert str(exc_info.value) == expected_message


def test_pascal_to_snake_case():
    test_cases = (
        # From PascalCase with digits
        ("A2", "a_2"),
        ("AB2", "a_b_2"),
        ("AB2D", "a_b_2d"),
        ("AB2DEf", "a_b_2d_ef"),
        ("Abc2", "abc_2"),
        ("Abc2D", "abc_2d"),
        ("Abc2Def", "abc_2def"),
        # From PascalCase without dot delimiter
        ("AbcDef", "abc_def"),
        # From PascalCase with dot delimiter
        ("Abc.Def", "abc.def"),
        ("AbcDef.Xyz", "abc_def.xyz"),
        ("AbcDef.UvwXyz", "abc_def.uvw_xyz"),
    )

    for input_value, expected in test_cases:
        assert CaseUtil.pascal_to_snake_case(input_value) == expected


def test_snake_to_pascal_case():
    test_cases = (
        # From snake_case with digits
        ("a_2", "A2"),
        ("a_b_2", "AB2"),
        ("a_b_2d", "AB2D"),
        ("a_b_2d_ef", "AB2DEf"),
        ("abc_2", "Abc2"),
        ("abc_2d", "Abc2D"),
        ("abc_2def", "Abc2Def"),
        # From snake_case without dot delimiter
        ("abc_def", "AbcDef"),
        # From snake_case with dot delimiter
        ("abc.def", "Abc.Def"),
        ("abc_def.xyz", "AbcDef.Xyz"),
        ("abc_def.uvw_xyz", "AbcDef.UvwXyz"),
        ("node_id", "NodeId"),
    )

    for input_value, expected in test_cases:
        assert CaseUtil.snake_to_pascal_case(input_value) == expected


def test_pascal_to_title_case():
    test_cases = (
        ("A2", "A 2"),
        ("AB2", "A B 2"),
        ("AB2D", "A B 2D"),
        ("AB2DEf", "A B 2D Ef"),
        ("Abc2", "Abc 2"),
        ("Abc2D", "Abc 2D"),
        ("Abc2Def", "Abc 2Def"),
    )

    for input_value, expected in test_cases:
        assert CaseUtil.pascal_to_title_case(input_value) == expected


def test_upper_to_snake_case():
    """Test for case conversion from UPPER_CASE to snake_case."""

    # From UPPER_CASE without dot delimiter
    assert CaseUtil.upper_to_snake_case("ABC_DEF") == "abc_def"

    # From UPPER_CASE with dot delimiter
    assert CaseUtil.upper_to_snake_case("ABC_DEF.XYZ") == "abc_def.xyz"


def test_upper_to_pascal_case():
    """Test for case conversion from UPPER_CASE to PascalCase."""

    # From UPPER_CASE without dot delimiter
    assert CaseUtil.upper_to_pascal_case("ABC_DEF") == "AbcDef"

    # From UPPER_CASE with dot delimiter
    assert CaseUtil.upper_to_pascal_case("ABC_DEF.XYZ") == "AbcDef.Xyz"


def test_pascal_to_upper_case():
    """Test for case conversion from PascalCase to UPPER_CASE."""

    # From UPPER_CASE without dot delimiter
    assert CaseUtil.pascal_to_upper_case("AbcDef") == "ABC_DEF"

    # From UPPER_CASE with dot delimiter
    assert CaseUtil.pascal_to_upper_case("AbcDef.Xyz") == "ABC_DEF.XYZ"


def test_check_snake_case():
    # Valid cases
    CaseUtil.check_snake_case("valid_snake_case_1")
    CaseUtil.check_snake_case("another_valid_3d_case_2_3")

    # Invalid cases
    check_raises_error(
        CaseUtil.check_snake_case,
        "invalid snake case",
        "String invalid snake case is not snake_case because it contains a space.",
    )
    check_raises_error(
        CaseUtil.check_snake_case,
        "InvalidSnakeCase",
        "String InvalidSnakeCase is not snake_case because it contains an uppercase character.",
    )
    check_raises_error(
        CaseUtil.check_snake_case,
        "invalid__snake_case",
        "String invalid__snake_case is not snake_case because it contains a doubled underscore.",
    )
    check_raises_error(
        CaseUtil.check_snake_case,
        "invalid_snake_case2",
        "String invalid_snake_case2 is not snake_case because it does not follow custom rule "
        "for separators in front of digits.",
    )


def test_check_pascal_case():
    # Valid cases
    CaseUtil.check_pascal_case("ValidPascalCase")
    CaseUtil.check_pascal_case("AnotherValidPascalCase")
    CaseUtil.check_pascal_case("AnotherValidPascalCaseWithDigits2")

    # Invalid cases
    check_raises_error(
        CaseUtil.check_pascal_case,
        "Invalid Pascal Case",
        "String Invalid Pascal Case is not PascalCase because it contains a space.",
    )
    check_raises_error(
        CaseUtil.check_pascal_case,
        "invalid_pascal_case",
        "String 'invalid_pascal_case' is not 'PascalCase' because it contains non-alphanumeric characters: '_'",
    )
    check_raises_error(
        CaseUtil.check_pascal_case,
        "invalidPascalcase",
        "String invalidPascalcase is not PascalCase because the first letter is lowercase.",
    )


def test_check_title_case():
    # Valid cases
    CaseUtil.check_title_case("Title Case Example 1")
    CaseUtil.check_title_case("Another Example 2")

    # Invalid cases
    check_raises_error(
        CaseUtil.check_title_case,
        "invalid_title_case",
        "String 'invalid_title_case' is not 'Title Case' because it contains non-alphanumeric characters: '_'",
    )
    check_raises_error(
        CaseUtil.check_title_case,
        "invalid Title Case",
        "String invalid Title Case is not Title Case because the first letter is lowercase.",
    )
    check_raises_error(
        CaseUtil.check_title_case,
        "Invalid Title Case2",
        "String Invalid Title Case2 is not Title Case because it does not follow custom rule "
        "for separators in front of digits.",
    )


def test_check_upper_case():
    # Valid cases
    CaseUtil.check_upper_case("VALID_UPPER_CASE_1")
    CaseUtil.check_upper_case("UPPER_CASE_3D_EXAMPLE_2")

    # Invalid cases
    check_raises_error(
        CaseUtil.check_upper_case,
        "Invalid_UPPER_CASE",
        "String Invalid_UPPER_CASE is not UPPER_CASE because it contains a lowercase character.",
    )
    check_raises_error(
        CaseUtil.check_upper_case,
        "UPPER_CASE example",
        "String UPPER_CASE example is not UPPER_CASE because it contains a space.",
    )
    check_raises_error(
        CaseUtil.check_upper_case,
        "UPPER_CASE2",
        "String UPPER_CASE2 is not UPPER_CASE because it does not follow custom rule for separators in front of digits.",
    )


def test_round_trip_conversions():
    pascal_to_snake_case_test_cases = (
        # From PascalCase with digits
        ("A2", "a_2"),
        ("AB2", "a_b_2"),
        ("AB2D", "a_b_2d"),
        ("AB2DEf", "a_b_2d_ef"),
        ("Abc2", "abc_2"),
        ("Abc2D", "abc_2d"),
        ("Abc2Def", "abc_2def"),
        # From PascalCase without dot delimiter
        ("AbcDef", "abc_def"),
        # From PascalCase with dot delimiter
        ("Abc.Def", "abc.def"),
        ("AbcDef.Xyz", "abc_def.xyz"),
        ("AbcDef.UvwXyz", "abc_def.uvw_xyz"),
    )
    snake_to_upper_case_test_cases = (
        # From snake_case with digits
        ("a_2", "A_2"),
        ("a_b_2", "A_B_2"),
        ("a_b_2d", "A_B_2D"),
        ("a_b_2d_ef", "A_B_2D_EF"),
        ("abc_2", "ABC_2"),
        ("abc_2d", "ABC_2D"),
        ("abc_2def", "ABC_2DEF"),
        # From snake_case without dot delimiter
        ("abc_def", "ABC_DEF"),
        # From snake_case with dot delimiter
        ("abc.def", "ABC.DEF"),
        ("abc_def.xyz", "ABC_DEF.XYZ"),
        ("abc_def.uvw_xyz", "ABC_DEF.UVW_XYZ"),
    )
    pascal_to_upper_case_test_cases = (
        # From PascalCase with digits
        ("A2", "A_2"),
        ("AB2", "A_B_2"),
        ("AB2D", "A_B_2D"),
        ("AB2DEf", "A_B_2D_EF"),
        ("Abc2", "ABC_2"),
        ("Abc2D", "ABC_2D"),
        ("Abc2Def", "ABC_2DEF"),
        # From PascalCase without dot delimiter
        ("AbcDef", "ABC_DEF"),
        # From PascalCase with dot delimiter
        ("Abc.Def", "ABC.DEF"),
        ("AbcDef.Xyz", "ABC_DEF.XYZ"),
        ("AbcDef.UvwXyz", "ABC_DEF.UVW_XYZ"),
    )

    for pascal_case_value, snake_case_value in pascal_to_snake_case_test_cases:
        assert CaseUtil.pascal_to_snake_case(pascal_case_value) == snake_case_value
        assert CaseUtil.snake_to_pascal_case(snake_case_value) == pascal_case_value

    for snake_case_value, upper_case_value in snake_to_upper_case_test_cases:
        assert CaseUtil.snake_to_upper_case(snake_case_value) == upper_case_value
        assert CaseUtil.upper_to_snake_case(upper_case_value) == snake_case_value

    for pascal_case_value, upper_case_value in pascal_to_upper_case_test_cases:
        assert CaseUtil.pascal_to_upper_case(pascal_case_value) == upper_case_value
        assert CaseUtil.upper_to_pascal_case(upper_case_value) == pascal_case_value


def test_non_alphanumeric():
    """Test CaseUtil._check_non_alphanumeric."""

    # Underscore
    CaseUtil._check_non_alphanumeric("a_b", "sample_format", allow_underscore=True)  # Do not throw
    with pytest.raises(Exception):
        CaseUtil._check_non_alphanumeric("a_b", "sample_format")

    # Other characters
    with pytest.raises(Exception):
        CaseUtil._check_non_alphanumeric("abc\n", "sample_format")
    with pytest.raises(Exception):
        CaseUtil._check_non_alphanumeric("abc\rdef", "sample_format")
    with pytest.raises(Exception):
        CaseUtil._check_non_alphanumeric("\ufeffabc_def", "sample_format")


def test_describe_char():
    """Test CaseUtil._check_non_alphanumeric."""
    assert CaseUtil._describe_char("\n") == 'Newline'
    assert CaseUtil._describe_char("\r") == 'Carriage Return'
    assert CaseUtil._describe_char("\ufeff") == 'UTF-8 BOM'


if __name__ == "__main__":
    pytest.main([__file__])
