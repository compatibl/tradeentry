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

import dateparser
from dataclasses import dataclass

from cl.runtime import Context
from cl.runtime.exceptions.error_util import ErrorUtil
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.dataclasses_extensions import missing
from cl.convince.entries.entry import Entry


@dataclass(slots=True, kw_only=True)
class DateEntry(Entry):
    """Maps a date string specified by the user to a calendar date."""

    date: str | None = None
    """Date specified by the entry in ISO-8601 yyyy-mm-dd string format."""

    def run_generate(self) -> None:
        """Retrieve parameters from this entry and save the resulting entries."""
        if self.verified:
            raise UserError(f"Entry {self.entry_id} is marked as verified, run Unmark Verified before running Propose."
                            f"This is a safety feature to prevent overwriting verified entries. ")

        # TODO: Check if the entry already exists in DB

        # Parse date
        if date := dateparser.parse(self.description):
            self.date = date.strftime('%Y-%m-%d')
            Context.current().save_one(self)
        else:
            raise ErrorUtil.value_error(
                self.description,
                details=f"Date '{self.description}' can't be parsed.",
                value_name="date",
                method_name="run_generate",
                data_type=DateEntry.__name__,
            )
