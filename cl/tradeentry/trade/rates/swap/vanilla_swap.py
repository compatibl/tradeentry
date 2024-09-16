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
from cl.tradeentry.trade.rates.rates_index import RatesIndex
from cl.tradeentry.trade.trade import Trade


@dataclass(slots=True, kw_only=True)
class VanillaSwap(Trade):
    """Vanilla fixed for floating swap."""

    maturity_time: str | None = None
    """Time interval between spot date and unadjusted maturity date in standardized string format."""

    ccy: str | None = None
    """Currency in ISO three-letter format."""

    float_index: RatesIndex | None = None
    """Interest rate index used by the floating leg."""

    fixed_rate: float | None = None
    """Fixed rate in number format, or breakeven fixed rate if not specified."""

