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

from cl.tradeentry.entries.rates.rates_leg_pay_or_receive_entry_key import PayOrReceiveEntryKey
from cl.tradeentry.entries.rates.rates_effective_date_entry_key import EffectiveDateEntryKey
from cl.tradeentry.entries.rates.rates_maturity_date_entry_key import MaturityDateEntryKey
from cl.tradeentry.entries.rates.rates_leg_entry import LegEntry


@dataclass(slots=True, kw_only=True)
class SwapLegEntry(LegEntry):
    """Swap leg."""

    buy_sell: PayOrReceiveEntryKey | None = None
    """String representation of the Buy or Sell flag in the format specified by the user."""

    effective_date: EffectiveDateEntryKey | None = None
    """Trade or leg effective date defined as unadjusted date or time interval relative to another date."""

    maturity_date: MaturityDateEntryKey | None = None
    """Trade or leg maturity date defined as unadjusted date or time interval relative to another date."""

    payment_frequency: str | None = None
    """Payment frequency."""
