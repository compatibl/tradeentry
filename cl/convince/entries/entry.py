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

from abc import abstractmethod, ABC
from dataclasses import dataclass

from cl.convince.entries.entry_type_key import EntryTypeKey
from cl.runtime import Context
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.convince.entries.entry_key import EntryKey

_MAX_TITLE_LEN = 1000
"""Maximum length of the title."""

@dataclass(slots=True, kw_only=True)
class Entry(EntryKey, RecordMixin[EntryKey], ABC):
    """Contains title, body and supporting data of user entry along with the entry processing result."""

    entry_type: EntryTypeKey = missing()
    """Type of the entry (included in MD5 hash)."""

    title: str = missing()
    """Title of a long entry or complete description of a short one (included in MD5 hash)."""

    body: str | None = None
    """Optional body of the entry if not completely described by the title (included in MD5 hash)."""

    data: str | None = None
    """Optional supporting data in YAML format (included in MD5 hash)."""

    approved_by: UserKey | None = None
    """Use who recorded the approval."""

    def get_key(self) -> EntryKey:
        return EntryKey(entry_id=self.entry_id)

    def init(self) -> None:
        """Generate entry_id in 'type: title' format followed by an MD5 hash of body and data if present."""
        # Initial checks for the title
        if StringUtil.is_empty(self.title):
            raise UserError("Empty 'Entry.title' field.")
        if len(self.title) > _MAX_TITLE_LEN:
            raise UserError(
                f"The length {len(self.title)} of the 'Entry.title' field exceeds {_MAX_TITLE_LEN}, "
                f"use 'Entry.body' field for the excess text."
            )
        if "\n" in self.title:
            raise UserError(f"Parameter title={self.title} of 'EntryUtil.create_id' method is not a single line.")

        if not StringUtil.is_empty(self.body) or not StringUtil.is_empty(self.data):
            # Append MD5 hash in hexadecimal format of the body and data if at least one is present
            md5_hash = StringUtil.md5_hex(f"{self.body}.{self.data}")
            self.entry_id = f"{self.title} (MD5: {md5_hash})"
        else:
            # Otherwise entry_id is the title
            self.entry_id = self.title

    @abstractmethod
    def run_propose(self) -> None:
        """Generate or regenerate the proposed value."""

    def run_approve(self) -> None:
        """Approve the manually set approved value, or proposed value if the approved value is not set."""
        # Set approved_py to the user obtained from the current context and save
        context = Context.current()
        self.approved_by = context.user
        context.save_one(self)
