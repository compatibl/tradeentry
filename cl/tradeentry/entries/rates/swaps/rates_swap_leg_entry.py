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
from dataclasses import dataclass

from cl.tradeentry.entries.pay_freq_entry_key import PayFreqEntryKey
from cl.tradeentry.entries.pay_receive_entry_key import PayReceiveEntryKey
from cl.tradeentry.entries.rates.rates_effective_date_entry_key import RatesEffectiveDateEntryKey
from cl.tradeentry.entries.rates.rates_leg_entry import RatesLegEntry
from cl.tradeentry.entries.rates.rates_maturity_date_entry_key import RatesMaturityDateEntryKey


@dataclass(slots=True, kw_only=True)
class RatesSwapLegEntry(RatesLegEntry):
    """Swap leg."""

    pay_receive: PayReceiveEntryKey | None = None
    """String representation of the Buy or Sell flag in the format specified by the user."""

    effective_date: RatesEffectiveDateEntryKey | None = None
    """Trade or leg effective date defined as unadjusted date or time interval relative to another date."""

    maturity_date: RatesMaturityDateEntryKey | None = None
    """Trade or leg maturity date defined as unadjusted date or time interval relative to another date."""

    pay_freq: PayFreqEntryKey | None = None
    """Payment frequency."""
