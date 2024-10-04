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
from cl.convince.entries.entry import Entry
from cl.convince.entries.entry_status_enum import EntryStatusEnum
from cl.tradeentry.entries.rates.rates_trade_type_entry import RatesTradeTypeEntry
from cl.tradeentry.entries.rates.swaps.vanilla.vanilla_swap_entry import VanillaSwapEntry
from cl.tradeentry.entries.trade_entry import TradeEntry
from cl.tradeentry.trades.rates.rates_trade_type_key import RatesTradeTypeKey
from cl.tradeentry.trades.rates.rates_trade_type_keys import RatesTradeTypeKeys
from cl.tradeentry.trades.rates.swaps.vanilla.vanilla_swap import VanillaSwap
from cl.tradeentry.trades.trade_key import TradeKey


@dataclass(slots=True, kw_only=True)
class RatesTradeEntry(TradeEntry):
    """Capture an interest rate trade from user input, trade type is determined from the input."""

    def process(self) -> None:
        # Recognize trade
        # TODO: Update to use AI
        rates_trade_type_entry = RatesTradeTypeEntry(entry_text=self.entry_text, parent_entry=self)
        rates_trade_type_entry.process()
        if rates_trade_type_entry.entry_status == EntryStatusEnum.COMPLETED:
            # Create and process trade entry record for the specific rates trade type
            # TODO: Use switch
            if rates_trade_type_entry.rates_trade_type == RatesTradeTypeKeys.vanilla_swap:
                vanilla_swap_entry = VanillaSwapEntry(entry_text=self.entry_text, parent_entry=self)
                vanilla_swap_entry.process()
            else:
                raise RuntimeError(f"Unknown asset class {rates_trade_type_entry.rates_trade_type.rates_trade_type_id}")

            # Copy the trade to this record
            self.trade = vanilla_swap_entry.trade
