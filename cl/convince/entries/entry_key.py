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
from dataclasses import dataclass
from typing import Type

from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin
from cl.runtime.records.protocols import is_key

_MAX_TITLE_LEN = 1000
"""Maximum length of the title."""

_DISALLOWED_TITLE_SUBSTRINGS = {
    ":": "Colon",
    "(": "Left parenthesis",
    ")": "Right parenthesis",
    "\n": "End of line",
    "\r": "Carriage return",
}
"""These substrings are not allowed in title."""

_ENTRY_ID_RE = re.compile(r"^([A-Za-z0-9_]+):\s([A-Za-z0-9\s]+)(?:\s\(MD5:\s([a-f0-9]{32})\))?$")
"""Regex for entry_id."""


@dataclass(slots=True, kw_only=True)
class EntryKey(KeyMixin):
    """Contains title, body and supporting data of user entry along with the entry processing result."""

    entry_id: str = missing()
    """Based on record type, title and MD5 hash of body and data if present, EntryUtil.create_id is used to generate."""

    def init(self) -> None:
        # Check only if inside a key, will be set automatically if inside a record
        if is_key(self):
            self.check_entry_id(self.entry_id)

    @classmethod
    def get_key_type(cls) -> Type:
        return EntryKey

    @classmethod
    def get_entry_id(
            cls,
            record_type: str,
            title: str,
            body: str | None = None,
            data: str | None = None,
    ) -> str:
        """Create the unique identifier from parameters."""

        # Initial checks for the title
        if StringUtil.is_empty(title):
            raise UserError(f"Empty 'title' field in {record_type}.")
        if len(title) > _MAX_TITLE_LEN:
            raise UserError(
                f"The length {len(title)} of the 'title' field in {record_type} exceeds {_MAX_TITLE_LEN}, "
                f"use 'Entry.body' field for the excess text."
            )
        title_substrings = [name for sub, name in _DISALLOWED_TITLE_SUBSTRINGS.items() if sub in title]
        if title_substrings:
            title_substrings_str = "\n".join(title_substrings)
            raise UserError(f"Field 'title' contains the following disallowed substrings:\n{title_substrings_str}\n. "
                            f"Field text:\n{title}")

        # Combine ClassName with title
        type_and_title = f"{record_type}: {title}"

        if not StringUtil.is_empty(body) or not StringUtil.is_empty(data):
            # Append MD5 hash in hexadecimal format of the body and data if at least one is present
            md5_hash = StringUtil.md5_hex(f"{body}.{data}")
            entry_id = f"{type_and_title} (MD5: {md5_hash})"
        else:
            # Otherwise use type and title only
            entry_id = type_and_title
        return entry_id

    @classmethod
    def check_entry_id(cls, entry_id: str) -> None:
        """Check that the unique identifier is compliant with the expected format."""
        if not re.match(_ENTRY_ID_RE, entry_id):
            raise UserError(
                f"EntryId format must be either 'RecordType: Title' or 'RecordType: Title (MD5: ...)'.\n"
                f"EntryId value: '{entry_id}'")
