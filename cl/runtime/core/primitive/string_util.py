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
from typing import List, Pattern

__first_cap_re: Pattern = re.compile('(.)([A-Z][a-z]+)')
__all_cap_re: Pattern = re.compile('([a-z0-9])([A-Z])')
__to_pascal_re: Pattern = re.compile('(?:^|_+)(.)')

eol: str = '\n'
"""Literal string for newline."""


def to_pascal_case(name: str) -> str:
    """Converts strings to PascalCase also removing underscores. No spaces expected."""
    return __to_pascal_re.sub(lambda match: f'{match.group(1).upper()}', name)


def to_snake_case(name: str) -> str:
    """Converts PascalCase strings to snake_case. No spaces expected."""
    s1: str = __first_cap_re.sub(r'\1_\2', name)
    result: str = __all_cap_re.sub(r'\1_\2', s1).lower()
    return result


def split_by_uppercase(value: str) -> List[str]:
    """Splits input string by any uppercase char."""

    parts = re.findall('[A-Z][^A-Z]*', value)
    if value and not parts:
        parts = [value]

    return parts


def list_to_label(headers: List[str]) -> List[str]:
    """
    Convert strings to words separated by space that start from upper case for all elements of input list.
    """

    return [header_to_label(header) for header in headers]


def header_to_label(header: str) -> str:
    """
    Convert string to words separated by space that start from upper case for all elements of input list.
    """
    return ' '.join(re.findall(r'[A-Z][^A-Z]*', to_pascal_case(header)))


def replace_prefix(value: str, old_prefix: str, new_prefix: str) -> str:
    """Replaces old prefix with new if it starts with it, otherwise returns as is."""
    if value.startswith(old_prefix):
        return new_prefix + value[len(old_prefix) :]
    return value
