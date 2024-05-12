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
import datetime as dt
from typing import Tuple

# Compile the regex pattern for YYYY-MM-DD
date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class DateUtil:
    """Util class for datetime.date."""

    @staticmethod
    def validate_str(date_str: str) -> None:
        """Validate that the date is in ISO-8601 yyyy-mm-dd format."""
        if not date_pattern.match(date_str):
            raise RuntimeError(f"Date string {date_str} is not in ISO-8601 yyyy-mm-dd format.")

    @staticmethod
    def to_iso_int(value: dt.date) -> int:
        """Convert from dt.date to yyyymmdd int."""
        return 10_000 * value.year + 100 * value.month + value.day

    @staticmethod
    def from_iso_int(iso_int: int) -> dt.date:
        """Convert from yyyymmdd int to dt.date."""

        # Convert to fields first
        year, month, day = DateUtil._iso_int_to_fields(iso_int)

        # Construct the date object which will also validate the date
        result: dt.date = dt.date(year, month, day)
        return result

    @staticmethod
    def to_str(value: dt.date) -> str:
        """Convert from dt.date to ISO-8601 yyyy-mm-dd string."""
        result: str = value.isoformat()
        return result

    @staticmethod
    def from_str(value_str: str) -> dt.date:
        """Convert from ISO-8601 yyyy-mm-dd string to dt.date."""

        # Convert using 'fromisoformat' method, this will also validate
        return dt.date.fromisoformat(value_str)

    @staticmethod
    def from_fields(year: int, month: int, day: int) -> dt.date:
        """Convert from year, month, and date fields to dt.date."""
        return dt.date(year, month, day)

    @staticmethod
    def _iso_int_to_fields(value: int) -> Tuple[int, int, int]:
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
