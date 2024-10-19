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
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.tradeentry.entries.pay_receive_entry_key import PayReceiveEntryKey
from cl.tradeentry.trades.pay_receive_key import PayReceiveKey


@dataclass(slots=True, kw_only=True)
class PayReceiveEntry(PayReceiveEntryKey, RecordMixin[PayReceiveEntryKey]):
    """User input to determine if we pay or receive payments or periodic coupons for a trade or leg."""

    value: PayReceiveKey = missing()
    """Flag indicating if we pay or receive payments or periodic coupons for a trade or leg."""

    def get_key(self) -> PayReceiveEntryKey:
        return PayReceiveEntryKey(entry_id=self.entry_id)
