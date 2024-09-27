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

from math import log10
import numpy as np


class FloatUtil:
    """
    This class provides standard serialization, parsing, and
    tolerance-based comparison for float values.

    Due to the performance overhead of Python classes, static
    class FloatUtil operating on native float variables
    should be used for any performance-critical applications.
    """

    empty: float = -1.0e100
    """Constant representing the empty value in non-nullable variables."""

    tolerance: float = 1.0e-10
    """
    Constant representing absolute float comparison tolerance.

    Rounding will change the value by not more than FloatUtil.tolerance.
    """

    tolerance_digits: int = int(round(-log10(tolerance)))
    """
    Constant representing decimal places in absolute float comparison tolerance.

    Rounding will change the value by not more than FloatUtil.tolerance.
    """

    @classmethod
    def format(cls, value: float) -> str:
        """
        Standard float serialization format, keeps only tolerance_digits decimal places.
        This will change the value by not more than FloatUtil.tolerance.
        """
        result = np.format_float_positional(
            value,
            precision=FloatUtil.tolerance_digits,
            unique=True,
            fractional=True,
            trim=".",
        )
        return result

    @classmethod
    def equal(cls, value_1: float, value_2: float) -> bool:
        """Returns true if the value_1 is closer than tolerance to value_2."""
        return value_2 - cls.tolerance < value_1 < value_2 + cls.tolerance

    @classmethod
    def less(cls, value_1: float, value_2: float) -> bool:
        """Returns true if the value_1 is less than value_2 minus tolerance."""
        return value_1 < value_2 - cls.tolerance

    @classmethod
    def less_or_equal(cls, value_1: float, value_2: float) -> bool:
        """Returns true if the value_1 is less than value_2 plus tolerance."""
        return value_1 < value_2 + cls.tolerance

    @classmethod
    def more(cls, value_1: float, value_2: float) -> bool:
        """Returns true if the value_1 is more than value_2 plus tolerance."""
        return value_1 > value_2 + cls.tolerance

    @classmethod
    def more_or_equal(cls, value_1: float, value_2: float) -> bool:
        """Returns true if the value_1 is more than value_2 minus tolerance."""
        return value_1 > value_2 - cls.tolerance

    @classmethod
    def get_int(cls, value: float) -> int:
        """Convert float to int if within tolerance from int, error otherwise."""
        result = int(round(value))
        if not cls.equal(result, value):
            raise RuntimeError(f"Cannot convert {value} to int because it is not within roundoff tolerance of an int.")
        return result
