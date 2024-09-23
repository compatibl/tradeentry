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

from typing import Dict
from typing import List


def fields_to_text(fields: List[Dict]) -> str:
    """
    [{"name": "NAME", "type": "TYPE", "freq": "FREQUENCY"}]
    ->
    "* NAME: TYPE, FREQUENCY"
    """
    strings = []
    for desc in fields:
        new_string = f"* {desc['name']}: {desc['type']}, {desc['freq']}"
        strings.append(new_string)
    return "\n".join(strings)


def tag_text_with_numbers(text):
    words = text.split()
    tagged_words = []

    for i, word in enumerate(words, start=1):
        tagged_words.append(f"<TAG_{i}>{word}</TAG_{i}>")

    return " ".join(tagged_words)


def add_line_numbers(text):
    lines = text.splitlines()
    numbered_lines = []

    for i, line in enumerate(lines, start=1):
        numbered_lines.append(f"{i}: {line}")

    return "\n".join(numbered_lines)
