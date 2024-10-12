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

_DESCRIPTION_MAP = {
    '\x00': 'Null Byte',
    '\n': 'Newline',
    '\t': 'Tab',
    '\r': 'Carriage Return',
    '\ufeff': 'UTF-8 BOM',
    '\uFFFD': 'Unicode replacement character',
    '\u201C': 'Left Double Quotation Mark',
    '\u201D': 'Right Double Quotation Mark',
}
"""Map of special unprintable characters to their descriptions."""

_FLAGGED_CHARS = [
    '\x00',  # Null Byte
    '\uFFFD',  # Unicode replacement character
]
"""List of characters that will trigger an error during normalization."""

_REMOVED_CHARS = [
    '\r',  # Carriage Return
    '\ufeff',  # UTF-8 BOM
    '\u201C',  # Left Double Quotation Mark
    '\u201D',  # Right Double Quotation Mark
]
"""List of characters that will be removed during normalization."""

_REPLACED_CHARS = {
    '\t': "    ",  # Tab
}
"""List of characters that will be replaced during normalization and their replacements."""

_FLAGGED_CHARS_REGEX = f"[{''.join(_FLAGGED_CHARS)}]"


class CharUtil:
    """Utilities for working with single characters."""

    @classmethod
    def normalize_chars(cls, value: str) -> str:
        """Flag _FLAGGED_CHARS, remove _REMOVED_CHARS and _REPLACED_CHARS. """

        # Search for flagged characters
        flagged_chars = list(set(re.findall(_FLAGGED_CHARS_REGEX, value)))
        if flagged_chars:
            flagged_char_names = ', '.join(CharUtil.describe_char(char) for char in flagged_chars)
            raise RuntimeError(f"The following characters are not allowed in input text: "
                               f"{flagged_char_names}")

        # Create a translation table for replacement
        translation_table = str.maketrans(_REPLACED_CHARS)

        # Apply the translation table to replace characters
        value = value.translate(translation_table)

        # Remove characters from _REMOVED_CHARS by translating them to None
        removal_table = str.maketrans('', '', ''.join(_REMOVED_CHARS))

        # Apply the removal translation
        return value.translate(removal_table)

    @classmethod
    def describe_char(cls, char: str) -> str:
        """If the character is in the special map, use its name, otherwise use repr()."""
        return _DESCRIPTION_MAP.get(char, repr(char))
