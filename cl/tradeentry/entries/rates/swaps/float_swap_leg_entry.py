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

from cl.convince.entries.entry_key import EntryKey
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.retrievers.annotating_retriever import AnnotatingRetriever
from cl.runtime import Context
from cl.tradeentry.entries.date_entry import DateEntry
from cl.tradeentry.entries.date_or_tenor_entry import DateOrTenorEntry
from cl.tradeentry.entries.pay_freq_entry import PayFreqEntry
from cl.tradeentry.entries.pay_receive_fixed_entry import PayReceiveFixedEntry
from cl.tradeentry.entries.rates.rates_index_entry import RatesIndexEntry
from cl.tradeentry.entries.rates.rates_spread_entry import RatesSpreadEntry
from cl.tradeentry.entries.rates.swaps.rates_swap_leg_entry import RatesSwapLegEntry
from cl.tradeentry.trades.rates.rates_leg_key import RatesLegKey

_SIDE = "The words Buy or Sell, or the words Pay or Receive"
_MATURITY = "Either maturity date as a date, or tenor (length) as the number of years and/or months"
_EFFECTIVE_DATE = "Effective date as date"
_PAY_FREQ = "Payment frequency"
_FLOAT_FREQ = "Frequency at which floating interest accrues"
_FLOAT_INDEX = "Floating rate index"
_FLOAT_SPREAD = "Spread over the interest rate index"


@dataclass(slots=True, kw_only=True)
class FloatSwapLegEntry(RatesSwapLegEntry):
    """A series of interest rate payments with a floating coupon based on an interest rate index.."""

    float_freq: EntryKey | None = None
    """Frequency at which floating interest accrues."""

    float_index: EntryKey | None = None
    """Floating interest rate index ('float_spread' is added to the index fixing)."""

    float_spread: EntryKey | None = None
    """Spread over the interest rate index (zero if not specified)."""

    def run_generate(self) -> None:
        """Retrieve parameters from this entry and save the resulting entries."""

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

        # Pay or receive flag
        if pay_receive_description := retriever.retrieve(input_text=input_text,
                                                         param_description=_SIDE,
                                                         is_required=False):
            pay_receive = PayReceiveFixedEntry(description=pay_receive_description)
            context.save_one(pay_receive)
            self.pay_receive = pay_receive.get_key()

        # Payment Frequency
        if pay_freq_description := retriever.retrieve(input_text=input_text,
                                                      param_description=_PAY_FREQ,
                                                      is_required=False):
            pay_freq = PayFreqEntry(description=pay_freq_description)
            context.save_one(pay_freq)
            self.pay_freq = pay_freq.get_key()

        # Floating Frequency
        if float_freq_description := retriever.retrieve(input_text=input_text,
                                                        param_description=_FLOAT_FREQ,
                                                        is_required=False):
            float_freq = PayFreqEntry(description=float_freq_description)
            context.save_one(float_freq)
            self.float_freq = float_freq.get_key()

        # Floating rate index
        if float_index_description := retriever.retrieve(input_text=input_text,
                                                         param_description=_FLOAT_INDEX,
                                                         is_required=False):
            float_index = RatesIndexEntry(description=float_index_description)
            context.save_one(float_index)
            self.float_index = float_index.get_key()

        # Floating rate spread
        if float_spread_description := retriever.retrieve(input_text=input_text,
                                                          param_description=_FLOAT_SPREAD,
                                                          is_required=False):
            float_spread = RatesSpreadEntry(
                description=float_spread_description
            )
            context.save_one(float_spread)
            self.float_spread = float_spread.get_key()

        # Save self to DB
        Context.current().save_one(self)
