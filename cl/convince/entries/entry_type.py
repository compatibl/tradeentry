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

from abc import ABC
from dataclasses import dataclass
from cl.runtime import RecordMixin
from cl.convince.entries.entry_type_key import EntryTypeKey


@dataclass(slots=True, kw_only=True)
class EntryType(EntryTypeKey, RecordMixin[EntryTypeKey], ABC):
    """Unique entry type is assigned to each purpose of user input."""

    description: str | None = None
    """Description of the entry type."""

    def get_key(self) -> EntryTypeKey:
        return EntryTypeKey(entry_type_id=self.entry_type_id)
