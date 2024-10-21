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

from dataclasses import dataclass
from cl.runtime import RecordMixin
from cl.runtime.log.log_entry_key import LogEntryKey
from cl.runtime.log.log_entry_level_enum import LogEntryLevelEnum
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.records.dataclasses_extensions import missing


@dataclass(slots=True, kw_only=True)
class LogEntry(LogEntryKey, RecordMixin[LogEntryKey]):
    """
    Refers to a record that captures specific information
    about events or actions occurring within an application.
    """

    level: LogEntryLevelEnum = missing()
    """A type of event."""

    message: str = missing()
    """A descriptive message providing details about the event."""

    def get_key(self) -> LogEntryKey:
        return LogEntryKey(timestamp=self.timestamp)

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""
        if self.timestamp is None:
            self.timestamp = OrderedUuid.to_readable_str(OrderedUuid.create_one())
