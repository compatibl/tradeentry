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
from cl.runtime import Context
from cl.convince.entries.entry_key import EntryKey
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.retrievers.annotating_retriever import AnnotatingRetriever
from cl.runtime.log.exceptions.user_error import UserError
from cl.tradeentry.entries.date_or_tenor_entry import DateOrTenorEntry
from cl.tradeentry.entries.fixed_rate_entry import FixedRateEntry
from cl.tradeentry.entries.pay_receive_fixed_entry import PayReceiveFixedEntry
from cl.tradeentry.entries.rates.rates_index_entry import RatesIndexEntry
from cl.tradeentry.entries.trade_entry import TradeEntry

_SIDE = ("The words Buy or Sell, or the words Pay Fixed (which for this trade type means Buy) "
         "or Receive Fixed (which for this trade type means Sell).")
_MATURITY = "Either maturity date as a date, or tenor (length) as the number of years and/or months"
_FLOAT_INDEX = "Floating rate index"
_FIXED_RATE = "Fixed rate"


@dataclass(slots=True, kw_only=True)
class VanillaSwapEntry(TradeEntry):
    """Vanilla fixed-for-floating swap."""

    pay_receive_fixed: EntryKey | None = None
    """String representation of the PayFixed or ReceiveFixed flag in the format specified by the user."""

    effective: EntryKey | None = None
    """Trade or leg effective date defined as unadjusted date or time interval relative to another date."""

    maturity: EntryKey | None = None
    """Trade or leg maturity date defined as unadjusted date or time interval relative to another date."""

    tenor: EntryKey | None = None
    """Swap tenor (length) in months or years."""

    float_index: EntryKey | None = None
    """Floating interest rate index or currency (in case of currency, default index for the currency is used)."""

    fixed_rate: EntryKey | None = None
    """Fixed rate entry or breakeven rate if not specified."""

    def run_generate(self) -> None:
        """Retrieve parameters from this entry and save the resulting entries."""
        if self.verified:
            raise UserError(f"Entry {self.entry_id} is marked as verified, run Unmark Verified before running Propose."
                            f"This is a safety feature to prevent overwriting verified entries. ")
        # Get retriever
        # TODO: Make configurable
        retriever = AnnotatingRetriever(
            retriever_id="test_annotating_retriever",
            llm=GptLlm(llm_id="gpt-4o"),
        )
        retriever.init_all()

        # Process fields
        context = Context.current()
        input_text = self.get_text()

        # Pay or receive fixed flag is described side
        pay_receive_fixed = PayReceiveFixedEntry(
            description=retriever.retrieve(
                input_text=input_text,
                param_description=_SIDE,
                is_required=False,
            )
        )
        context.save_one(pay_receive_fixed)
        self.pay_receive_fixed = pay_receive_fixed.get_key()

        # Tenor
        maturity = DateOrTenorEntry(
            description=retriever.retrieve(
                input_text=input_text,
                param_description=_MATURITY,
                is_required=False,
            )
        )
        context.save_one(maturity)
        self.maturity = maturity.get_key()

        # Floating rate index
        float_index = RatesIndexEntry(
            description=retriever.retrieve(
                input_text=input_text,
                param_description=_FLOAT_INDEX,
                is_required=False,
            )
        )
        context.save_one(float_index)
        self.float_index = float_index.get_key()

        # Fixed Rate
        fixed_rate = FixedRateEntry(
            description=retriever.retrieve(
                input_text=input_text,
                param_description=_FIXED_RATE,
                is_required=False,
            )
        )
        context.save_one(fixed_rate)
        self.fixed_rate = fixed_rate.get_key()

        # Save self to DB
        Context.current().save_one(self)
