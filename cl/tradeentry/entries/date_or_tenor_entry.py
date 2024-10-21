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
from cl.convince.entries.entry import Entry


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
