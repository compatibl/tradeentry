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
from cl.tradeentry.entries.rates.rates_index_entry_key import RatesIndexEntryKey
from cl.tradeentry.entries.rates.rates_spread_entry_key import RatesSpreadEntryKey
from cl.tradeentry.entries.rates.swaps.rates_swap_leg_entry import RatesSwapLegEntry


@dataclass(slots=True, kw_only=True)
class FloatSwapLegEntry(RatesSwapLegEntry):
    """A series of interest rate payments with a floating coupon based on an interest rate index.."""

    float_freq: str | None = None
    """Frequency at which floating interest accrues."""

    float_index: RatesIndexEntryKey | None = None
    """Floating interest rate index ('float_spread' is added to the index fixing)."""

    float_spread: RatesSpreadEntryKey | None = None
    """Spread over the interest rate index."""
