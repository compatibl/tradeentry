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

from cl.runtime import Context
from cl.convince.entries.entry_key import EntryKey
from cl.tradeentry.entries.trade_entry import TradeEntry


@dataclass(slots=True, kw_only=True)
class VanillaSwapEntry(TradeEntry):
    """Vanilla fixed-for-floating swap."""

    pay_receive_fixed: EntryKey | None = None
    """String representation of the PayFixed or ReceiveFixed flag in the format specified by the user."""

    effective_date: EntryKey | None = None
    """Trade or leg effective date defined as unadjusted date or time interval relative to another date."""

    maturity_date: EntryKey | None = None
    """Trade or leg maturity date defined as unadjusted date or time interval relative to another date."""

    float_index: EntryKey | None = None
    """Floating interest rate index or currency (in case of currency, default index for the currency is used)."""

    fixed_rate: EntryKey | None = None
    """Fixed rate entry or breakeven rate if not specified."""

    @classmethod
    def create(
            cls,
            title: str,
            *,
            body: str | None = None,
            data: str | None = None,
    ) -> Self:
        # TODO: This is a stub, requires implementation

        # Create an instance of self and populate fields of the base class
        result = cls.create_self(title, body=body, data=data)

        # TODO: Populate fields

        # Save to storage and return
        Context.current().save_one(result)
        return result

