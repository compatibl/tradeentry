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
import re
from typing import Tuple

# Compile the regex pattern for date in ISO-8601 format yyyy-mm-dd
date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class DateUtil:
    """Utility class for dt.date."""

    @classmethod
    def to_str(cls, value: dt.date) -> str:
        """Convert to string in ISO-8601 format: 'yyyy-mm-dd'"""
        result = f"{value.year:04}-{value.month:02}-{value.day:02}"
        return result

    @classmethod
    def from_str(cls, value: str) -> dt.date:
        """Convert from string in ISO-8601 format: 'yyyy-mm-dd'"""

        # Validate string format
        cls.validate_str(value)

        # Convert to date using strict parsing
        result = dt.date.fromisoformat(value)
        return result

    @classmethod
    def to_fields(cls, value: dt.date) -> Tuple[int, int, int]:
        """Convert dt.date to fields."""
        return value.year, value.month, value.day

    @classmethod
    def from_fields(cls, year: int, month: int, day: int) -> dt.date:
        """Convert fields to dt.date."""

        result = dt.date(year, month, day)
        return result

    @classmethod
    def to_iso_int(cls, value: dt.date) -> int:
        """Convert dt.date in yyyymmdd format."""
        result = 1_00_00 * value.year + 1_00 * value.month + value.day
        return result

    @classmethod
    def from_iso_int(cls, value: int) -> dt.date:
        """Convert int in yyyymmdd format."""

        if value < 10000000:
            raise RuntimeError(f"Date {value} is too short for 'yyyymmdd' format.")
        if value > 99999999:
            raise RuntimeError(f"Date {value} is too long for 'yyyymmdd' format.")

        year: int = value // 1_00_00
        value -= year * 1_00_00
        if year > 9999 or year < 1899:
            raise RuntimeError(f"Invalid year {year} for date {value} in 'yyyymmdd' format.")

        month: int = value // 1_00
        value -= month * 1_00
        if month > 12 or month < 1:
            raise RuntimeError(f"Invalid month {month} for date {value} in 'yyyymmdd' format.")

        day: int = value
        if day > 31 or day < 1:
            raise RuntimeError(f"Invalid day {day} for date {value} in 'yyyymmdd' format.")

        result = dt.date(year, month, day)
        return result

    @classmethod
    def validate_str(cls, value: str) -> None:
        """Validate that date string is in ISO-8601 format: 'yyyy-mm-dd'"""
        if not date_pattern.match(value):
            raise RuntimeError(f"Date string {value} must be in ISO-8601 format: 'yyyy-mm-dd'.")
