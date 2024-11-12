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
from cl.runtime.exceptions.error_util import ErrorUtil
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.float_util import FloatUtil
from cl.convince.entries.entry import Entry
from cl.convince.entries.entry_key import EntryKey
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.retrievers.annotating_retriever import AnnotatingRetriever
from cl.tradeentry.entries.currency_entry import CurrencyEntry
from cl.tradeentry.entries.number_entry import NumberEntry
from cl.tradeentry.trades.currency import Currency

_AMOUNT = """Numerical value of the amount (including possible space, commas and other
decimal point and thousands separators between digits) or its text representation (e.g. 'ten') 
including any scale unit such as  'm' or 'millions', 'b' or 'bn' or 'billions' but excluding any
currency symbols such as '$', 'USD' or 'dollars'.

Ensure you do not include anything other than digits and scale units, even if additional non-digit
symbols such as a currency symbol are not separated by a space from the digits which may happen
especially with the currency amount.

Pay attention to the examples where you initially provided an incorrect answer:

Input: $100m
Your answer: {$100}m
Correct answer: ${100m}

Input: USD 100,000,000
Your answer: USD {100},000,000
Correct answer: USD {100,000,000}
"""

_CURRENCY = """Currency symbol, natural language description or ISO-4217 code.
Semicolon-delimited examples: $; dollar; USD
"""


@dataclass(slots=True, kw_only=True)
class AmountEntry(Entry):
    """Amount with or without currency specification."""

    amount: EntryKey | None = None
    """Numerical value for the amount excluding any units multiplier or currency (e.g. '10' for '$10m')."""

    currency: EntryKey | None = None
    """Optional entry for the currency if specified along with the amount (e.g. '$' for '$10m')."""

    def run_generate(self) -> None:
        """Retrieve parameters from this entry and save the resulting entries."""

        if self.verified:
            raise UserError(
                f"Entry {self.entry_id} is marked as verified, run Unmark Verified before running Generate."
                f"This is a safety feature to prevent overwriting verified entries. "
            )

        # Get retriever
        context = Context.current()
        retriever = AnnotatingRetriever(
            retriever_id="AnnotatingRetriever",
            llm=GptLlm(llm_id="gpt-4o"),
        )
        retriever.init_all()

        # Process fields
        input_text = self.get_text()

        # Currency symbol preprocessing to avoid JSON formatting issues
        # when the LLM attempts to escape the symbol (e.g. \$ or '\$')
        # TODO: Use a configurable list
        input_text = input_text.replace("$US", "USD")
        input_text = input_text.replace("$", "USD")
        input_text = input_text.replace("$CA", "CAD")
        input_text = input_text.replace("€", "EUR")

        # Any unverified component will set this field to False
        verified = True

        # Currency description
        currency_description = retriever.retrieve(
            input_text=input_text,
            param_description=_CURRENCY,
            is_required=False,
        )
        if currency_description is not None:
            # Try to load an existing entry using reverse lookup
            self.currency = CurrencyEntry.get_entry_key(currency_description)
            if (loaded := context.load_one(CurrencyEntry, self.currency, is_record_optional=True)) is None:
                # Save only if does not exist
                currency = CurrencyEntry(description=currency_description, lang=self.lang)
                context.save_one(currency)
            else:
                # Otherwise update the verified status
                verified = verified and loaded.verified

        # Extract the currency if present
        amount_description = retriever.retrieve(
            input_text=input_text,
            param_description=_AMOUNT,
            is_required=True,
        )
        if amount_description is not None:
            # Try to load an existing entry using reverse lookup
            self.amount = NumberEntry.get_entry_key(amount_description)
            if (loaded := context.load_one(NumberEntry, self.amount, is_record_optional=True)) is None:
                # Save only if does not exist
                amount = NumberEntry(description=amount_description, lang=self.lang)
                context.save_one(amount)
            else:
                # Otherwise update the verified status
                verified = verified and loaded.verified

        # Set verified status and save self to DB
        self.verified = verified
        Context.current().save_one(self)

    @classmethod
    def _parse_and_check_amount(cls, amount_str: str) -> float:
        """Convert to float value if provided as a string, detailed error message if the conversion fails."""
        try:
            # Convert and check the amount
            result = float(amount_str)
            cls._check_amount(result)
            return result
        except Exception as e:  # noqa
            # Rethrow with details
            raise ErrorUtil.value_error(
                amount_str,
                details=f"Conversion of amount to a floating number failed.\n{e}",
                value_name="amount",
                data_type=AmountEntry.__name__,
            )

    @classmethod
    def _check_amount(cls, amount: float) -> None:
        """Check numerical value of the amount, detailed error message if the check fails."""
        # Check range with tolerance
        if FloatUtil.less(amount, 0.0):
            raise ErrorUtil.value_error(
                amount,
                details=f"The amount is negative.",
                value_name="amount",
                data_type=AmountEntry.__name__,
            )
        elif FloatUtil.less(amount, 1.0):
            raise ErrorUtil.value_error(
                amount,
                details=f"""
The amount is less than one. Choosing the units that require fractional amounts 
is contrary to the capital markets conventions.""",
                value_name="amount",
                data_type=AmountEntry.__name__,
            )
