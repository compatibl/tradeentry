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
from cl.tradeentry.trades.pay_receive_fixed_key import PayReceiveFixedKey
from cl.tradeentry.trades.rates.rates_index_key import RatesIndexKey
from cl.tradeentry.trades.trade import Trade


@dataclass(slots=True, kw_only=True)
class VanillaSwap(Trade):
    """Vanilla fixed-for-floating swap."""

    pay_receive_fixed: PayReceiveFixedKey = missing()
    """Flag indicating if we pay or receive fixed leg coupons in a fixed-for-floating swap."""

    effective_date: dt.date = missing()
    """Effective date."""

    maturity_date: dt.date = missing()
    """Maturity date."""

    float_index: RatesIndexKey = missing()
    """Floating interest rate index."""

    fixed_rate_pct: float = missing()
    """Fixed rate in percent."""
