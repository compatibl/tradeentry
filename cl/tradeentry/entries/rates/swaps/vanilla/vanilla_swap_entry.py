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
from cl.tradeentry.entries.fixed_rate_entry_key import FixedRateEntryKey
from cl.tradeentry.entries.pay_receive_fixed_entry_key import PayReceiveFixedEntryKey
from cl.tradeentry.entries.rates.rates_effective_date_entry_key import RatesEffectiveDateEntryKey
from cl.tradeentry.entries.rates.rates_index_entry_key import RatesIndexEntryKey
from cl.tradeentry.entries.rates.rates_maturity_date_entry_key import RatesMaturityDateEntryKey
from cl.tradeentry.entries.trade_entry import TradeEntry


@dataclass(slots=True, kw_only=True)
class VanillaSwapEntry(TradeEntry):
    """Vanilla fixed-for-floating swap."""

    pay_receive_fixed: PayReceiveFixedEntryKey | None = None
    """String representation of the PayFixed or ReceiveFixed flag in the format specified by the user."""

    effective_date: RatesEffectiveDateEntryKey | None = None
    """Trade or leg effective date defined as unadjusted date or time interval relative to another date."""

    maturity_date: RatesMaturityDateEntryKey | None = None
    """Trade or leg maturity date defined as unadjusted date or time interval relative to another date."""

    float_index: RatesIndexEntryKey | None = None
    """Floating interest rate index or currency (in case of currency, default index for the currency is used)."""

    fixed_rate: FixedRateEntryKey | None = None
    """Fixed rate (breakeven rate is assumed if not specified)."""
