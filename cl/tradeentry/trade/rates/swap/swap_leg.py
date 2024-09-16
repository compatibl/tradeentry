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
from cl.tradeentry.trade.leg import Leg


@dataclass(slots=True, kw_only=True)
class SwapLeg(Leg):
    """Swap leg."""

    start_date: dt.date | None = None
    """Accrual start as unadjusted date."""

    start_time: str | None = None
    """Time interval between spot date and unadjusted start date in standardized string format."""

    maturity_date: dt.date | None = None
    """Maturity as unadjusted date."""

    maturity_time: str | None = None
    """Time interval between spot date and unadjusted maturity date in standardized string format."""

    maturity_length: str | None = None
    """Time interval between unadjusted start date and unadjusted maturity date in standardized string format."""

    pay_freq: str | None = None
    """Payment frequency in standardized string format."""
