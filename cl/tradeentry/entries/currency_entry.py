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

import re
from dataclasses import dataclass
from cl.runtime import Context
from cl.runtime.exceptions.error_util import ErrorUtil
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.dataclasses_extensions import missing
from cl.convince.entries.entry import Entry
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.retrievers.multiple_choice_retriever import MultipleChoiceRetriever
from cl.tradeentry.trades.currency import Currency
from cl.tradeentry.trades.currency_key import CurrencyKey

_CURRENCY_ISO_CODE = "Currency code in strict ISO-4217 format of three uppercase letters, no variations allowed."
"""Parameter description for the currency ISO-4217 code."""

_ISO_RE = re.compile(r"^[A-Z]{3}$")
"""Regex for the ISO-4217 currency code."""


@dataclass(slots=True, kw_only=True)
class CurrencyEntry(Entry):
    """Maps currency string specified by the user to the ISO-4217 three-letter currency code."""

    currency: CurrencyKey | None = missing()
    """Currency (output)."""

    def run_generate(self) -> None:
        """Retrieve parameters from this entry and save the resulting entries."""
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

        # Get the list of valid currency codes
        context = Context.current()
        currencies = context.load_all(Currency)
        iso_codes = [currency.iso_code for currency in currencies]

        # Retrieve ISO code
        input_text = self.get_text()
        retrieval = retriever.retrieve(
            input_text=input_text,
            param_description=_CURRENCY_ISO_CODE,
            valid_choices=iso_codes,
        )
        self._check_iso_code(retrieval.param_value)
        self.currency = CurrencyKey(iso_code=retrieval.param_value)

        # Save self to DB
        Context.current().save_one(self)

    @classmethod
    def _check_iso_code(cls, iso_code: str) -> None:
        """Check that the currency conforms to ISO-4217 specification and is on the list of known currencies."""
        # Check that iso_code conforms to the ISO-4217 format
        if not bool(_ISO_RE.match(iso_code)):
            raise ErrorUtil.value_error(
                iso_code,
                details=f"It must be a 3-letter uppercase ISO-4217 currency code.",
                value_name="iso_code",
                data_type=CurrencyEntry.__name__,
            )
        # Try to load a currency record, error if not found
        ccy = Context.current().load_one(Currency, CurrencyKey(iso_code=iso_code), is_record_optional=True)
        if ccy is None:
            raise ErrorUtil.value_error(
                iso_code,
                details=f"Currency record is not found for iso_code={iso_code}",
                value_name="iso_code",
                data_type=CurrencyEntry.__name__,
            )
