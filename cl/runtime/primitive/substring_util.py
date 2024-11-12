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

_SUBSTRING_NAMES = {
    ":": "Colon",
    "(": "Left parenthesis",
    ")": "Right parenthesis",
    "\n": "End of line",
    "\r": "Carriage return",
}
"""Readable names of substring characters for error reporting."""


class SubstringUtil:  # TODO: In progress, methods to be added
    """Utilities for detecting and reporting disallowed characters in substrings."""
