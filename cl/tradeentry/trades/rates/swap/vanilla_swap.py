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

from cl.tradeentry.formats.rates.fixed_rate_key import FixedRateKey
from cl.tradeentry.formats.schedule.date_key import DateKey
from cl.tradeentry.formats.schedule.time_interval_key import TimeIntervalKey
from cl.tradeentry.formats.symbols.currency_key import CurrencyKey
from cl.tradeentry.trades.rates.rates_index import RatesIndex
from cl.tradeentry.trades.trade import Trade


@dataclass(slots=True, kw_only=True)
class VanillaSwap(Trade):
    """Vanilla fixed for floating swap."""

    maturity_date: DateKey | None = None
    """Maturity as unadjusted date."""

    maturity_time: TimeIntervalKey | None = None
    """Time interval between spot date and unadjusted maturity date."""

    ccy: CurrencyKey | None = None
    """Currency of the swap."""

    float_index: RatesIndex | None = None
    """Interest rate index used by the floating leg."""

    fixed_rate: FixedRateKey | None = None
    """Fixed rate (breakeven rate is assumed if not specified)."""
