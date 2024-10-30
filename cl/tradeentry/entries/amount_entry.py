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
from cl.runtime.exceptions.error_util import ErrorUtil
from cl.runtime.primitive.float_util import FloatUtil
from cl.convince.entries.entry import Entry
from cl.convince.entries.entry_key import EntryKey


@dataclass(slots=True, kw_only=True)
class AmountEntry(Entry):
    """Amount with or without currency specification."""

    amount: float | None = None
    """Numerical value for the amount including any units multiplier (e.g. 1,000,000 for 1m)."""

    currency_entry: EntryKey | None = None
    """Optional entry for the currency if specified along with the amount."""

    def init(self) -> None:
        # Perform check only if the amount is set
        if self.amount is not None:

            # Convert to float value if provided as a string, detailed error message if the conversion fails
            if isinstance(self.amount, str):
                try:
                    self.amount = float(self.amount)
                except Exception as e:  # noqa
                    # Rethrow with details
                    raise ErrorUtil.value_error(
                        self.amount,
                        details=f"Conversion of amount to a floating number failed.\n{e}",
                        value_name="amount",
                        data_type=AmountEntry.__name__,
                    )

            # Check range with tolerance
            if FloatUtil.less(self.amount, 0.0):
                raise ErrorUtil.value_error(
                    self.amount,
                    details=f"The amount is negative.",
                    value_name="amount",
                    data_type=AmountEntry.__name__,
                )
            elif FloatUtil.less(self.amount, 1.0):
                raise ErrorUtil.value_error(
                    self.amount,
                    details=f"""
    The amount is less than one. Choosing the units that require fractional amounts 
    is contrary to the capital markets conventions.""",
                    value_name="amount",
                    data_type=AmountEntry.__name__,
                )
