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
from cl.convince.entries.entry_key import EntryKey
from cl.tradeentry.entries.rates.rates_leg_entry import RatesLegEntry


@dataclass(slots=True, kw_only=True)
class RatesSwapLegEntry(RatesLegEntry, ABC):
    """Swap leg."""

    pay_receive: EntryKey | None = None
    """String representation of the Buy or Sell flag in the format specified by the user."""

    effective_date: EntryKey | None = None
    """Trade or leg effective date defined as unadjusted date or time interval relative to another date."""

    maturity_date: EntryKey | None = None
    """Trade or leg maturity date defined as unadjusted date or time interval relative to another date."""

    pay_freq: EntryKey | None = None
    """Payment frequency."""
