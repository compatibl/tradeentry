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

from cl.tradeentry.trades.rates.rates_trade_type_key import RatesTradeTypeKey


class RatesTradeTypeKeys:
    """Standard interest rate trade type keys."""

    vanilla_swap: RatesTradeTypeKey = RatesTradeTypeKey(rates_trade_type_id="VanillaSwap")
    """Vanilla fixed-for-floating swap."""

    fixed_for_floating_swap: RatesTradeTypeKey = RatesTradeTypeKey(rates_trade_type_id="FixedForFloatingSwap")
    """Fixed-for-floating interest rate swap with features outside the vanilla swap type."""

    fixed_for_fixed_swap: RatesTradeTypeKey = RatesTradeTypeKey(rates_trade_type_id="FixedForFixedSwap")
    """Fixed-for-fixed interest rate swap."""

    basis_swap: RatesTradeTypeKey = RatesTradeTypeKey(rates_trade_type_id="BasisSwap")
    """Interest rate basis swap where both parties pay floating."""
