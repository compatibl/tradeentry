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

from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.retrievers.annotating_retriever import AnnotatingRetriever
from cl.runtime import Context
from cl.runtime.exceptions.error_util import ErrorUtil
from cl.runtime.primitive.float_util import FloatUtil
from cl.convince.entries.entry import Entry
from cl.convince.entries.entry_key import EntryKey

_NUMERICAL_VALUE = """Numerical value of the amount (e.g. '10') or its text representation (e.g. 'ten') 
excluding any currency symbols such as '$', 'USD' or 'dollars' and excluding any units (multiplier) such as 
'm' or 'millions', 'b' or 'bn' or 'billions'.
Ensure you do not include anything other than digits, even if additional non-digit symbols are not
separated by a space from the digits which may happen especially with the currency amount.

Pay attention to the examples where you initially provided an incorrect answer:

Input: $100m
Your answer: {$100}m
Correct answer: ${100}m

Input: USD 100,000,000
Your answer: USD {100},000,000
Correct answer: USD {100,000,000}
"""
_CURRENCY = "Currency as ISO-4217 code or natural language description if present."


@dataclass(slots=True, kw_only=True)
class AmountEntry(Entry):
    """Amount with or without currency specification."""

    amount: float | None = None  # TODO: Make it number entry
    """Numerical value for the amount excluding any units multiplier or currency (e.g. '10' for '$10m')."""

    units_entry: EntryKey | None = None
    """Optional entry for the units specified along with the numerical amount (e.g. 'm' for '$10m')."""

    currency_entry: EntryKey | None = None
    """Optional entry for the currency if specified along with the amount (e.g. '$' for '$10m')."""

    def init(self) -> None:
        # Perform amount checks only if it is set
        if self.amount is not None:
            if isinstance(self.amount, float):
                # Check value
                self._check_amount(self.amount)
            elif isinstance(self.amount, int):
                # Check value after converting to float
                self._check_amount(float(self.amount))
            elif isinstance(self.amount, str):
                # Convert to float value and check value
                self.amount = self._parse_and_check_amount(self.amount)
            else:
                raise ErrorUtil.value_error(
                    self.amount,
                    details=f"The amount is neither a string nor a numerical value.",
                    value_name="amount",
                    data_type=AmountEntry.__name__,
                )

    def run_propose(self) -> None:
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

        # Extract the amount
        amount_str = retriever.retrieve(
            input_text=input_text,
            param_description=_NUMERICAL_VALUE,
            is_required=True,
        )
        self.amount = self._parse_and_check_amount(amount_str)

        # Save self to DB
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
