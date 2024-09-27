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
from typing import List
from typing import Pattern

_first_cap_re: Pattern = re.compile("(.)([A-Z][a-z]+)")
_all_cap_re: Pattern = re.compile("([a-z0-9])([A-Z])")
_to_pascal_re: Pattern = re.compile("(?:^|_+)(.)")

eol: str = "\n"
"""Literal string for newline."""


class StringUtil:
    """Utilities for case conversion and other operations on string."""

    @classmethod
    def to_pascal_case(cls, value: str) -> str:
        """Converts each dot-delimited token to PascalCase by replacing underscores with capital letters."""
        input_tokens = value.split(".")
        result_tokens = [_to_pascal_re.sub(lambda match: f"{match.group(1).upper()}", x) for x in input_tokens]
        result = ".".join(result_tokens)
        return result

    @classmethod
    def to_snake_case(cls, value: str) -> str:
        """
        Converts each dot-delimited token to snake_case by inserting underscore before each capital
        letter and then changing case to lower.
        """
        input_tokens = value.split(".")
        result_tokens = [_first_cap_re.sub(r"\1_\2", x).lower() for x in input_tokens]
        result = ".".join(result_tokens)
        return result

    @classmethod
    def split_by_uppercase(cls, value: str) -> List[str]:
        """Splits input string by any uppercase char."""

        parts = re.findall("[A-Z][^A-Z]*", value)
        if value and not parts:
            parts = [value]

        return parts

    @classmethod
    def list_to_label(cls, headers: List[str]) -> List[str]:
        """
        Convert strings to words separated by space that start from upper case for all elements of input list.
        """

        return [cls.header_to_label(header) for header in headers]

    @classmethod
    def header_to_label(cls, header: str) -> str:
        """
        Convert string to words separated by space that start from upper case for all elements of input list.
        """
        return " ".join(re.findall(r"[A-Z][^A-Z]*", cls.to_pascal_case(header)))

    @classmethod
    def replace_prefix(cls, value: str, old_prefix: str, new_prefix: str) -> str:
        """Replaces old prefix with new if it starts with it, otherwise returns as is."""
        if value.startswith(old_prefix):
            return new_prefix + value[len(old_prefix) :]
        return value
