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
from cl.runtime.records.record_mixin import RecordMixin
from cl.tradeentry.entries.asset_class_entry_key import AssetClassEntryKey


@dataclass(slots=True, kw_only=True)
class AssetClassEntry(AssetClassEntryKey, RecordMixin[AssetClassEntryKey]):
    """Maps asset class string specified by the user to the standard asset class identifier."""

    def get_key(self) -> AssetClassEntryKey:
        return AssetClassEntryKey(entry_id=self.entry_id)
