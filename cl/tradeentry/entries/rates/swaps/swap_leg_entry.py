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

from cl.tradeentry.formats.buy_sell_key import BuySellKey
from cl.tradeentry.formats.schedule.date_key import DateKey
from cl.tradeentry.formats.schedule.effective_date_key import EffectiveDateKey
from cl.tradeentry.formats.schedule.maturity_date_key import MaturityDateKey
from cl.tradeentry.formats.schedule.time_interval_key import TimeIntervalKey
from cl.tradeentry.trades.leg import Leg


@dataclass(slots=True, kw_only=True)
class SwapLeg(Leg):
    """Swap leg."""

    buy_sell: BuySellKey | None = None
    """String representation of the Buy or Sell flag in the format specified by the user."""

    effective_date: EffectiveDateKey | None = None
    """Trade or leg effective date defined as unadjusted date or time interval relative to another date."""

    maturity_date: MaturityDateKey | None = None
    """Trade or leg maturity date defined as unadjusted date or time interval relative to another date."""

    payment_frequency: str | None = None
    """Payment frequency."""
