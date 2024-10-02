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
from abc import abstractmethod
from dataclasses import dataclass
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.convince.entries.entry_key import EntryKey
from cl.convince.entries.entry_status_enum import EntryStatusEnum
from cl.convince.llms.llm_key import LlmKey


@dataclass(slots=True, kw_only=True)
class Entry(EntryKey, RecordMixin[EntryKey], ABC):
    """Performs comprehension of the specified type on entry text."""

    parent_entry: EntryKey | None = None
    """Parent entry (optional)."""

    entry_status: EntryStatusEnum = missing()
    """Entry type."""

    llm: LlmKey = missing()
    """LLM used to process the entry."""

    def __post_init__(self):
        """Populate status if not specified."""

        # Call __post_init__ from the base class
        super(Entry, self).__post_init__()

        if self.entry_status is None:
            self.entry_status = EntryStatusEnum.CREATED

    def get_key(self) -> EntryKey:
        return EntryKey(entry_type=self.entry_type, entry_text=self.entry_text)

    @abstractmethod
    def process(self) -> None:
        """Process using the LLM specified in the entry record."""
