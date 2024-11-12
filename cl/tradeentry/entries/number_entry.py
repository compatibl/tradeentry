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
from text_to_num import text2num
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

_NUMBER_WITH_SUFFIX_RE = re.compile(
    r"(\d+(\.\d+)?)([kmb]|mm|bb|bn|thousand|thousands|mil|million|millions|billion|billions)?"
)
"""Matches a number with decimal point separator and suffixes."""


@dataclass(slots=True, kw_only=True)
class NumberEntry(Entry):
    """Number specified using words or digits."""

    value: float | None = missing()
    """Numerical value (output)."""

    def run_generate(self) -> None:
        """Retrieve parameters from this entry and save the resulting entries."""
        if self.verified:
            raise UserError(
                f"Entry {self.entry_id} is marked as verified, run Unmark Verified before running Propose."
                f"This is a safety feature to prevent overwriting verified entries. "
            )
        # First non-AI text2num library to parse a number with suffix
        if (value := self._parse_number_with_suffix(self.description)) is not None:
            # Use parsed value
            try:
                self.value = float(value)
            except Exception as e:  # noqa
                raise ErrorUtil.value_error(
                    self.description,
                    details=f"Numerical description of a number with suffix could not be parsed "
                    f"using language code {self.lang}.",
                    value_name="number",
                    method_name="run_generate",
                    data_type=NumberEntry.__name__,
                )
        else:
            # Try to parse a word description
            try:
                value = text2num(self.description, self.lang)
                self.value = float(value)
            except Exception as e:  # noqa
                raise ErrorUtil.value_error(
                    self.description,
                    details=f"Text description of a number could not be parsed using language code {self.lang}.",
                    value_name="number",
                    method_name="run_generate",
                    data_type=NumberEntry.__name__,
                )

        # Save
        Context.current().save_one(self)

    def _parse_number_with_suffix(self, description: str) -> float | None:
        """Parse number with suffix for thousands, million or billion."""

        # TODO: Adjust for non-US number conventions
        # Remove comma thousands separator
        description = description.replace(",", "")

        # Convert to lowercase and match to regex
        description = description.lower()
        # TODO: Make regex and scale unit mapping dependent on self.lang
        match = _NUMBER_WITH_SUFFIX_RE.match(description)
        if match:
            number, _, scale_unit = match.groups()
            try:
                # Try to convert to float
                number = float(number)
            except Exception as e:  # noqa
                raise ErrorUtil.value_error(
                    self.description,
                    details=f"Text description of a number could not be parsed using language code {self.lang}.",
                    value_name="number",
                    method_name="run_generate",
                    data_type=NumberEntry.__name__,
                )
            if scale_unit is None:
                # No scale units, return as is
                return number
            elif scale_unit.lower() in ["k", "thousand", "thousands"]:
                # Thousands
                return number * 1_000
            elif scale_unit.lower() in ["m", "mm", "mil", "million", "millions"]:
                # Millions
                return number * 1_000_000
            elif scale_unit.lower() in ["b", "bb", "bn", "billion", "billions"]:
                return number * 1_000_000_000  # Billions (single 'b' or 'bn')
            else:
                raise ErrorUtil.value_error(
                    self.description,
                    details=f"Unknown number scale units '{scale_unit}'.",
                    value_name="scale_unit",
                    method_name="run_generate",
                    data_type=NumberEntry.__name__,
                )
        else:
            # Return None if not a number with suffix
            return None
