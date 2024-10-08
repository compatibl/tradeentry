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

from __future__ import annotations
from dataclasses import dataclass
from typing import Type

from cl.convince.entries.entry_type_key import EntryTypeKey
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin
from cl.runtime.records.protocols import is_record


@dataclass(slots=True, kw_only=True)
class EntryKey(KeyMixin):
    """Contains title, body and supporting data along with the results of their processing."""

    entry_id: str = missing()
    """Uses 'type: title' format followed by an MD5 hash of body and data if present."""

    @classmethod
    def get_key_type(cls) -> Type:
        return EntryKey

    @classmethod
    def create_key(
            cls,
            entry_type: EntryTypeKey,
            title: str,
            *,
            body: str | None = None,
            data: str | None = None
    ) -> EntryKey:
        """Uses 'type: title' format followed by an MD5 hash of body and data if present."""

        # Initial checks
        if entry_type is None:
            raise RuntimeError("Empty 'entry_type' is passed to 'EntryKey.create_key' method.")
        if StringUtil.is_empty(title):
            raise RuntimeError("Empty 'title' is passed to 'EntryKey.create_key' method.")

        # Type and title
        entry_id = f"{entry_type.entry_type_id}: {title}"

        # Append MD5 hash in hexadecimal format of the body and data if present
        if not StringUtil.is_empty(body) or not StringUtil.is_empty(data):
            md5_hash = StringUtil.md5_hex(f"{body}.{data}")
            entry_id = f"{entry_id} (MD5: {md5_hash})"

        # Return key
        return EntryKey(entry_id=entry_id)
