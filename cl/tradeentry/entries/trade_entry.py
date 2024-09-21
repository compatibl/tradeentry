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
from cl.tradeentry.trades.asset_class_key import AssetClassKey
from cl.tradeentry.trades.rates.swaps.vanilla.vanilla_swap import VanillaSwap
from cl.tradeentry.trades.trade_key import TradeKey


@dataclass(slots=True, kw_only=True)
class TradeEntry(Entry):
    """Capture trade from user input."""

    trade: TradeKey | None = None
    """Trade captured from the entry (populated during processing)."""

    def process(self) -> None:
        # Recognize asset class
        asset_class_entry = AssetClassEntry(entry_text=self.entry_text, parent_entry=self)
        asset_class_entry.process()
        if asset_class_entry.entry_status == EntryStatusEnum.Completed:
            # TODO: Use switch
            if asset_class_entry.asset_class == AssetClassKey(asset_class_id="Rates"):
                self.trade = VanillaSwap()
            else:
                raise RuntimeError(f"Unknown asset class {asset_class_entry.asset_class.asset_class_id}")
