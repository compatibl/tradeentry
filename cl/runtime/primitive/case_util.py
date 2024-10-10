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

import re
from typing import Pattern

from cl.runtime.primitive.string_util import StringUtil

_all_cap_re: Pattern = re.compile(r"([a-z])([A-Z])")
# Pattern to add underscores before digits (e.g., "Abc2" -> "abc_2")
_digit_separator_re: Pattern = re.compile(r"([a-zA-Z])(\d)")
# This pattern looks for uppercase sequences and adds an underscore between them if needed
_consecutive_cap_re: Pattern = re.compile(r"([A-Z])([A-Z])")
# Digit without underscore pattern
_digit_without_underscore_re: Pattern = re.compile(r"(?<!_)\d")
# Digit without space pattern
_digit_without_space_re: Pattern = re.compile(r"(?<! )\d")


class CaseUtil:
    """Utilities for case conversion and other operations on string."""

    @classmethod
    def pascal_to_snake_case(cls, value: str | None) -> str | None:
        """Convert PascalCase to snake_case using custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            return value
        cls.check_pascal_case(value)
        # Add underscores between consecutive uppercase letters
        result = _consecutive_cap_re.sub(r"\1_\2", value)
        # Handle lowercase to uppercase transitions
        result = _all_cap_re.sub(r"\1_\2", result)
        # Insert underscore before digits
        result = _digit_separator_re.sub(r"\1_\2", result)

        # Convert the final result to lowercase
        return result.lower()

    @classmethod
    def upper_to_snake_case(cls, value: str | None) -> str | None:
        """Convert UPPER_CASE to snake_case using custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            return value
        cls.check_upper_case(value)
        return value.lower()

    @classmethod
    def snake_to_upper_case(cls, value: str | None) -> str | None:
        """Convert snake_case to UPPER_CASE using custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            return value
        cls.check_snake_case(value)
        return value.upper()

    @classmethod
    def snake_to_pascal_case(cls, value: str | None) -> str | None:
        """Convert snake_case to PascalCase using custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            return value
        cls.check_snake_case(value)
        input_tokens = value.split(".")

        # Apply the processing (i.e. `__pascalize_segment()`) function to each segment and join
        # them into PascalCase.
        # Finally, join the tokens with dots and return the result
        return ".".join(
            ["".join(cls.__pascalize_segment(segment) for segment in token.split("_")) for token in input_tokens]
        )

    @classmethod
    def upper_to_pascal_case(cls, value: str | None) -> str | None:
        """Convert UPPER_CASE to PascalCase using custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            return value
        cls.check_upper_case(value)
        return cls.snake_to_pascal_case(value.lower())

    @classmethod
    def pascal_to_upper_case(cls, value: str | None) -> str | None:
        """Convert PascalCase to UPPER_CASE using custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            return value
        cls.check_pascal_case(value)
        snake_case_value = cls.pascal_to_snake_case(value)
        return snake_case_value.upper()

    @classmethod
    def pascal_to_title_case(cls, value: str | None) -> str | None:
        """Convert PascalCase to Title Case using custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            return value
        cls.check_pascal_case(value)
        snake_case_value = cls.pascal_to_snake_case(value)

        # Apply the processing (i.e. `__pascalize_segment()`) function to each segment and join
        # them into Title Case.
        return " ".join(cls.__pascalize_segment(segment) for segment in snake_case_value.split("_"))

    @classmethod
    def snake_to_title_case(cls, value: str | None) -> str | None:
        """Convert snake_case to Title Case using custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            return value
        cls.check_snake_case(value)
        pascal_case_value = cls.snake_to_pascal_case(value)
        return cls.pascal_to_title_case(pascal_case_value)

    @classmethod
    def check_snake_case(cls, value: str | None) -> None:
        """Error message if arg is not snake_case or does not follow custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            # Consider None or empty string compliant with the format
            return
        cls._check_no_space(value, "snake_case")
        cls._check_no_upper(value, "snake_case")
        cls._check_double_underscore(value, "snake_case")
        cls._check_snake_case_digit_separator(value)

    @classmethod
    def check_pascal_case(cls, value: str | None) -> None:
        """Error message if arg is not PascalCase or does not follow custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            # Consider None or empty string compliant with the format
            return
        cls._check_no_space(value, "PascalCase")
        cls._check_no_underscore(value, "PascalCase")
        cls._check_first_letter_capitalized(value, "PascalCase")
        # NOTE: PascalCase shouldn't be checked for custom rule for separators in
        # front of digits, because there's no separators

    @classmethod
    def check_title_case(cls, value: str | None) -> None:
        """Error message if arg is not Title Case or does not follow custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            # Consider None or empty string compliant with the format
            return
        cls._check_no_underscore(value, "Title Case")
        cls._check_first_letter_capitalized(value, "Title Case")
        cls._check_title_case_digit_separator(value)

    @classmethod
    def check_upper_case(cls, value: str | None) -> None:
        """Error message if arg is not UPPER_CASE or does not follow custom rule for separators in front of digits."""
        if StringUtil.is_empty(value):
            # Consider None or empty string compliant with the format
            return
        cls._check_no_space(value, "UPPER_CASE")
        cls._check_no_lower(value, "UPPER_CASE")
        cls._check_upper_case_digit_separator(value)

    @classmethod
    def is_pascal_case(cls, value: str) -> bool:
        """Check if the string is in PascalCase."""
        try:
            cls.check_pascal_case(value)
            return True
        except RuntimeError:
            return False

    @classmethod
    def is_snake_case(cls, value: str) -> bool:
        """Check if the string is in snake_case."""
        try:
            cls.check_snake_case(value)
            return True
        except RuntimeError:
            return False

    @classmethod
    def is_title_case(cls, value: str) -> bool:
        """Check if the string is in Title Case."""
        try:
            cls.check_title_case(value)
            return True
        except RuntimeError:
            return False

    @classmethod
    def is_upper_case(cls, value: str) -> bool:
        """Check if the string is in UPPER_CASE."""
        try:
            cls.check_upper_case(value)
            return True
        except RuntimeError:
            return False

    @classmethod
    def _check_no_space(cls, value: str, format_: str) -> None:
        """Error message stating string does not follow format if it contains a space."""
        if " " in value:
            raise RuntimeError(f"String {value} is not {format_} because it contains a space.")

    @classmethod
    def _check_no_underscore(cls, value: str, format_: str) -> None:
        """Error message stating string does not follow format if it contains an underscore."""
        if "_" in value:
            raise RuntimeError(f"String {value} is not {format_} because it contains an underscore.")

    @classmethod
    def _check_double_underscore(cls, value: str, format_: str) -> None:
        """Error message stating string does not follow format if it contains a double underscore."""
        if "__" in value:
            raise RuntimeError(f"String {value} is not {format_} because it contains a doubled underscore.")

    @classmethod
    def _check_no_lower(cls, value: str, format_: str) -> None:
        """Error message stating string does not follow format if it contains a lowercase character."""
        if any(char.islower() for char in value):
            raise RuntimeError(f"String {value} is not {format_} because it contains a lowercase character.")

    @classmethod
    def _check_no_upper(cls, value: str, format_: str) -> None:
        """Error message stating string does not follow format if it contains an uppercase character."""
        if any(char.isupper() for char in value):
            raise RuntimeError(f"String {value} is not {format_} because it contains an uppercase character.")

    @classmethod
    def _check_first_letter_capitalized(cls, value: str, format_: str) -> None:
        """Error message stating string does not follow format if it does not start with an uppercase letter."""
        if not value[0].isupper():
            raise RuntimeError(f"String {value} is not {format_} because the first letter is lowercase.")

    @classmethod
    def _check_snake_case_digit_separator(cls, value: str) -> None:
        """Error message stating string does not follow custom rule for separators in front of digits"""
        # snake_case must have an underscore in front of digits
        if _digit_without_underscore_re.search(value):
            raise RuntimeError(
                f"String {value} is not snake_case because it does not follow custom rule "
                f"for separators in front of digits.",
            )

    @classmethod
    def _check_title_case_digit_separator(cls, value: str) -> None:
        """Error message stating string does not follow custom rule for separators in front of digits"""
        # Title Case must have a space in front of digits
        if _digit_without_space_re.search(value):
            raise RuntimeError(
                f"String {value} is not Title Case because it does not follow custom rule "
                f"for separators in front of digits.",
            )

    @classmethod
    def _check_upper_case_digit_separator(cls, value: str) -> None:
        """Error message stating string does not follow custom rule for separators in front of digits"""
        # Make a round trip from snake_case to PascalCase and back to snake_case to check
        # if the value stays the same
        if _digit_without_underscore_re.search(value):
            raise RuntimeError(
                f"String {value} is not UPPER_CASE because it does not follow custom rule "
                f"for separators in front of digits.",
            )

    @staticmethod
    def __pascalize_segment(segment: str) -> str:
        """
        Pascalize a segment (substring between 2 underscores) from snake_case
        using custom rule for separators in front of digits.
        """
        # If the segment starts with a digit, capitalize only the first character after the digit
        if segment and segment[0].isdigit():
            return segment[0] + segment[1:].capitalize()
        # Otherwise, capitalize the first letter of the segment
        return segment.capitalize()
