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
from typing_extensions import Self
from cl.convince.entries.entry import Entry
from cl.convince.entries.entry_key import EntryKey
from cl.runtime import Context
from cl.tradeentry.trades.asset_class_key import AssetClassKey
from cl.tradeentry.trades.asset_class_keys import AssetClassKeys  # TODO: Use AssetClassKeys


@dataclass(slots=True, kw_only=True)
class AssetClassEntry(Entry):
    """Capture asset class from user input for the entire trade."""

    asset_class: AssetClassKey | None = None
    """Asset class captured from the entry."""

    asset_class_entry: EntryKey | None = None
    """Asset-class-specific entry using the same title, body and data."""
