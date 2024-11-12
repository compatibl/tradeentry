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
from cl.runtime.log.exceptions.user_error import UserError
from cl.convince.entries.entry import Entry
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.retrievers.multiple_choice_retriever import MultipleChoiceRetriever
from cl.tradeentry.trades.rates.rates_index_key import RatesIndexKey

_FLOAT_INDEX = "Name of the floating interest rate index"


@dataclass(slots=True, kw_only=True)
class RatesIndexEntry(Entry):
    """Floating interest rate index or currency (in case of currency, default index for the currency is used)."""

    rates_index: RatesIndexKey | None = None
    """Floating rate index."""

    def run_generate(self) -> None:
        if self.verified:
            raise UserError(
                f"Entry {self.entry_id} is marked as verified, run Unmark Verified before running Propose."
                f"This is a safety feature to prevent overwriting verified entries. "
            )
        # Get retriever
        # TODO: Make configurable
        retriever = MultipleChoiceRetriever(
            retriever_id="MultipleChoiceRetriever",
            llm=GptLlm(llm_id="gpt-4o"),
        )
        retriever.init_all()

        # List of valid options
        options = [
            "LIBOR",
            "EURIBOR",
            "SOFR",
            "EONIA",
            "TONAR",
            "SARON",
            "SONIA",
            "BBSW",
            "TIBOR",
            "SHIBOR",
            "MIBOR",
            "FIBOR",
            "HIBOR",
            "OIS",
            "WIBOR",
            "STIBOR",
            "BHKR",
            "ESTER",
            "SIBOR",
        ]

        # Retrieve index name
        input_text = self.get_text()
        retrieval = retriever.retrieve(
            input_text=input_text,
            param_description=_FLOAT_INDEX,
            valid_choices=options,
        )

        self.rates_index = RatesIndexKey(rates_index_id=retrieval.param_value)

        # Save self to DB
        Context.current().save_one(self)
