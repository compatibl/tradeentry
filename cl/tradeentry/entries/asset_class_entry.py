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
from cl.tradeentry.trades.asset_class_key import AssetClassKey
from cl.tradeentry.trades.asset_class_keys import AssetClassKeys


@dataclass(slots=True, kw_only=True)
class AssetClassEntry(Entry):
    """Capture asset class from user input for the entire trade."""

    asset_class: AssetClassKey | None = None
    """Asset class captured from the entry (populated during processing)."""

    def process(self) -> None:
        # Recognize asset class
        # TODO: Update to use AI
        if self.entry_text == "Swap":
            self.asset_class = AssetClassKeys.rates
        elif self.entry_text == "VanillaSwap":
            self.asset_class = AssetClassKeys.rates
        else:
            raise RuntimeError(f"Cannot extract asset class from {self.entry_text}")
        self.entry_status = EntryStatusEnum.COMPLETED
