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

_NUMERICAL_VALUE = "Numerical value of the amount excluding any units."
_CURRENCY = "Currency as ISO-4217 code or natural language description if present."


@dataclass(slots=True, kw_only=True)
class AmountEntry(Entry):
    """Amount with or without currency specification."""

    amount: float | None = None
    """Numerical value for the amount including any units multiplier (e.g. 1,000,000 for 1m)."""

    currency_entry: EntryKey | None = None
    """Optional entry for the currency if specified along with the amount."""

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

        # Pay or receive fixed flag is described side
        amount_str = retriever.retrieve(self.entry_id, input_text, _NUMERICAL_VALUE)
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
