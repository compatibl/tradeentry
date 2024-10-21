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

import hashlib
from typing import TypeGuard


class StringUtil:
    """Utilities for string, other than case conversion which is in CaseUtil."""

    @classmethod
    def is_empty(cls, value: str | None) -> bool:
        """Returns true if the string is None or ''."""
        return value is None or value == ""

    @classmethod
    def is_not_empty(cls, value: str | None) -> TypeGuard[str]:
        """Returns true if the string is not None or ''."""
        return value is not None and value != ""

    @classmethod
    def md5_hex(cls, value: str | None) -> str:
        """Return MD5 hash in hexadecimal format after converting to lowercase and removing all whitespace."""
        return cls._md5(value).hexdigest()

    @classmethod
    def _md5(cls, value: str | None):
        """Return MD5 hash object after converting to lowercase and removing all whitespace."""

        # Convert to lowercase and remove all whitespace including EOL for any OS
        value = value.lower()
        value = value.replace(" ", "").replace("\n", "").replace("\r", "")

        # Encode to bytes using UTF-8 and get the MD5 hash in hexadecimal format
        result = hashlib.md5(value.encode("utf-8"))
        return result
