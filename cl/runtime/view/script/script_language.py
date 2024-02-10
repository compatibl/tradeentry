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

from enum import IntEnum


class ScriptLanguage(IntEnum):
    """Script language."""

    R = 0
    """R language."""

    Json = 1
    """Json markup."""

    Xml = 2
    """Xml markup."""

    Python = 3
    """Python language."""

    Markdown = 4
    """Lightweight markup language."""

    Sql = 5
    """Sql."""

    Cpp = 6
    """C++ language."""

    C = 7
    """C language."""

    Csharp = 8
    """C# language."""

    Java = 9
    """Java language."""

    Typescript = 10
    """TypeScript language."""

    Javascript = 11
    """JavaScript language."""

    Plaintext = 12
    """Plaintext."""
