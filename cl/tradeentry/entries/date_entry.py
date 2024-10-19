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

import datetime as dt
from abc import ABC
from dataclasses import dataclass
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.tradeentry.entries.date_entry_key import DateEntryKey


@dataclass(slots=True, kw_only=True)
class DateEntry(DateEntryKey, RecordMixin[DateEntryKey], ABC):
    """Maps a date string specified by the user to a calendar date."""

    value: str = missing()
    """Date specified by the entry in ISO-8601 yyyy-mm-dd string format."""

    def get_key(self) -> DateEntryKey:
        return DateEntryKey(entry_id=self.entry_id)
