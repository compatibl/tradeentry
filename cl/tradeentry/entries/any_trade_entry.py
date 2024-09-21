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
from cl.tradeentry.entries.asset_class_entry import AssetClassEntry
from cl.tradeentry.entries.rates.rates_trade_entry import RatesTradeEntry
from cl.tradeentry.entries.trade_entry import TradeEntry
from cl.tradeentry.trades.asset_class_keys import AssetClassKeys
from cl.tradeentry.trades.trade_key import TradeKey


@dataclass(slots=True, kw_only=True)
class AnyTradeEntry(TradeEntry):
    """Capture trade for any asset class from user input, trade type is determined from the input."""

    def process(self) -> None:
        # Recognize trade
        # TODO: Update to use AI
        asset_class_entry = AssetClassEntry(entry_text=self.entry_text, parent_entry=self)
        asset_class_entry.process()
        if asset_class_entry.entry_status == EntryStatusEnum.Completed:
            # Create and process trade entry record for the specific trade type
            # TODO: Use switch
            if asset_class_entry.asset_class == AssetClassKeys.rates:
                rates_trade_entry = RatesTradeEntry(entry_text=self.entry_text, parent_entry=self)
                rates_trade_entry.process()
            else:
                raise RuntimeError(f"Unknown asset class {asset_class_entry.asset_class.asset_class_id}")

            # Copy the trade to this record
            self.trade = rates_trade_entry.trade
