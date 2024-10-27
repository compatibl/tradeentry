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
from cl.runtime.records.dataclasses_extensions import missing
from cl.convince.entries.entry import Entry
from cl.convince.entries.entry_key import EntryKey


@dataclass(slots=True, kw_only=True)
class AmountEntry(Entry):
    """Amount with or without currency specification."""

    amount: float = missing()
    """Numerical value for the amount including any units multiplier (e.g. 1,000,000 for 1m)."""

    currency_entry: EntryKey | None = None
    """Optional entry for the currency if specified along with the amount."""
