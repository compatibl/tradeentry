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

from abc import ABC
from dataclasses import dataclass
from cl.runtime.records.record_mixin import RecordMixin
from cl.tradeentry.trades.trade_key import TradeKey


@dataclass(slots=True, kw_only=True)
class Trade(TradeKey, RecordMixin[TradeKey], ABC):
    """A standalone trade or part of a basket or strategy (in the latter case, parent field will be specified)."""

    parent_trade: TradeKey | None = None
    """Specified for trades that are part of a basket or strategy (PV will be aggregated under the parent)."""

    def get_key(self) -> TradeKey:
        return TradeKey(trade_id=self.trade_id)
