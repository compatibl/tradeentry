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
from cl.runtime.records.dataclasses_extensions import missing
from cl.tradeentry.trades.freq_key import FreqKey
from cl.tradeentry.trades.pay_receive_key import PayReceiveKey
from cl.tradeentry.trades.rates.rates_leg import RatesLeg


@dataclass(slots=True, kw_only=True)
class RatesSwapLeg(RatesLeg):
    """Swap leg."""

    pay_receive: PayReceiveKey = missing()
    """Flag indicating if we pay or receive payments or periodic coupons for a trade or leg."""

    effective_date: str = missing()
    """Effective date in ISO-8601 yyyy-mm-dd string format."""

    maturity_date: str = missing()
    """Maturity date in ISO-8601 yyyy-mm-dd string format."""

    pay_freq: FreqKey = missing()
    """Payment frequency."""
