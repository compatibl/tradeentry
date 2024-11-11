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

from cl.runtime import Context
from cl.convince.entries.entry import Entry
from cl.tradeentry.entries.date_entry import DateEntry

_TENOR_RE = re.compile(r"(\d+)([ymwd])")


@dataclass(slots=True, kw_only=True)
class DateOrTenorEntry(Entry):
    """
    Can be specified as either a date or a tenor (length).

    Notes:
        - Fields are additive, however some combinations are not used in capital markets
    """

    date: str | None = None
    """The only field if specified as a date."""

    years: int | None = None
    """Years component of the time interval (either this field or date can be specified but not both)."""

    months: int | None = None
    """Months component of the time interval (either this field or date can be specified but not both)."""

    weeks: int | None = None
    """Weeks component of the time interval (either this field or date can be specified but not both)."""

    days: int | None = None
    """Days component of the time interval (either this field or date can be specified but not both)."""

    business_days: int | None = None
    """Business days component of the time interval (either this field or date can be specified but not both)."""

    def run_generate(self) -> None:
        # TODO: Check if the entry already exists in DB

        # Try to parse as tenor first
        if matches := re.findall(_TENOR_RE, self.description.lower()):

            matches_dict = {unit: num for num, unit in matches}

            # Set each field based on matches or set to None if not present
            self.years = int(matches_dict.get('y', 0)) or None
            self.months = int(matches_dict.get('m', 0)) or None
            self.weeks = int(matches_dict.get('w', 0)) or None
            self.days = int(matches_dict.get('d', 0)) or None
        else:
            date_entry = DateEntry(description=self.description)
            date_entry.run_generate()
            self.date = date_entry.date

        # Save
        Context.current().save_one(self)
