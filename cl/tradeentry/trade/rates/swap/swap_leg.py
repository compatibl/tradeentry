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

from cl.tradeentry.formats.schedule.date_key import DateKey
from cl.tradeentry.formats.schedule.time_interval_key import TimeIntervalKey
from cl.tradeentry.trade.leg import Leg


@dataclass(slots=True, kw_only=True)
class SwapLeg(Leg):
    """Swap leg."""

    start_date: DateKey | None = None
    """Accrual start as unadjusted date."""

    start_time: TimeIntervalKey | None = None
    """Time interval between spot date and unadjusted start date."""

    first_payment_date: DateKey | None = None
    """First payment date as unadjusted date."""

    first_payment_time: TimeIntervalKey | None = None
    """Time interval between spot date and unadjusted first payment date."""

    maturity_date: DateKey | None = None
    """Maturity as unadjusted date."""

    maturity_time: TimeIntervalKey | None = None
    """Time interval between spot date and unadjusted maturity date."""

    maturity_length: TimeIntervalKey | None = None
    """Time interval between unadjusted start date and unadjusted maturity date."""

    payment_freq: str | None = None
    """Payment frequency."""
