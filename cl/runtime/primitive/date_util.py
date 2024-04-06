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

import datetime as dt
from typing import Any
from typing import Tuple


class DateUtil:
    """Util class for datetime.date."""

    @staticmethod
    def validate(value: dt.date) -> None:
        pass

    @staticmethod
    def to_iso_int(value: dt.date) -> int:
        return 10_000 * value.year + 100 * value.month + value.day

    @staticmethod
    def from_iso_int(iso_int: int) -> Any:
        # Convert to tuple
        year, month, day = DateUtil._to_fields_lenient(iso_int)

        # This will also validate the date
        result: dt.date = dt.date(year, month, day)
        return result

    @staticmethod
    def to_str(value: dt.date) -> str:
        result: str = value.isoformat()
        return result

    @staticmethod
    def from_str(value_str: str) -> Any:
        if value_str.endswith("Z"):
            raise Exception(
                f"String {value_str} passed to dt.date ctor must not end with capital Z that "
                f"indicates UTC timezone because dt.date does not include timezone."
            )

        # Convert from string in yyyy-mm-dd format
        date_from_str: dt.date = dt.date.fromisoformat(value_str)
        return date_from_str

    @staticmethod
    def from_fields(year: int, month: int, day: int) -> dt.date:
        """Create from year, month, and date fields."""
        return dt.date(year, month, day)

    @staticmethod
    def _to_fields_lenient(value: int) -> Tuple[int, int, int]:
        """
        Convert dt.date represented as int in yyyymmdd format to
        the tuple (year, month, day).
        """

        year: int = value // 10_000
        value -= year * 10_000
        month: int = value // 100
        value -= month * 100
        day: int = value

        return year, month, day
