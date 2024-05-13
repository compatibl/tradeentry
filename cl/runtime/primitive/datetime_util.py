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
from typing import Optional
from typing import Tuple

# Compile the regex pattern for datetime in ISO-8601 format yyyy-mm-ddThh:mm:ss.fffZ
datetime_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")


class DatetimeUtil:
    """Utility class for dt.datetime."""

    @staticmethod
    def round(value: dt.datetime) -> dt.datetime:
        """Round to whole milliseconds (the argument must already be in UTC timezone)."""

        # Check timezone
        offset = value.utcoffset()
        if offset is None:
            raise RuntimeError(f"Datetime {value} does not specify timezone. "
                               f"Only UTC timezone is accepted and must be specified explicitly.")
        elif value.utcoffset().total_seconds() != 0:
            raise RuntimeError(f"Datetime {value} is in {value.tzname()} timezone."
                               f"Only UTC timezone is accepted and must be specified explicitly.")

        fractional_milliseconds_float = 1000.0 * value.second + value.microsecond / 1000.0
        rounded_microseconds = round(fractional_milliseconds_float)

        second: int = rounded_microseconds // 1_000
        rounded_microseconds -= second * 1_000
        if second > 59 or second < 0:
            raise RuntimeError(f"Invalid second {second} for datetime {value} after rounding.")

        millisecond: int = rounded_microseconds
        if millisecond > 999 or millisecond < 0:
            raise RuntimeError(f"Invalid millisecond {millisecond} for datetime {value} after rounding.")

        result = dt.datetime(value.year,  value.month, value.day, value.hour, value.minute,
                             second,  # New value from rounding
                             1_000 * millisecond, dt.timezone.utc  # New value from rounding
                             )
        return result

    @staticmethod
    def to_str(value: dt.datetime) -> str:
        """Convert to string in ISO-8601 format rounded to milliseconds: 'yyyy-mm-ddThh:mm:ss.fffZ'"""

        # Validate timezone and rounding to milliseconds
        DatetimeUtil.validate_datetime(value)

        # Already round number of milliseconds
        millisecond = value.microsecond // 1000

        # Convert to string
        result = (f"{value.year:04}-{value.month:02}-{value.day:02}"
                  f"T{value.hour:02}:{value.minute:02}:{value.second:02}.{millisecond:03}Z")
        return result

    @staticmethod
    def from_str(value: str) -> dt.datetime:
        """Convert from string in ISO-8601 format rounded to milliseconds: 'yyyy-mm-ddThh:mm:ss.fffZ'"""

        # Validate string format
        DatetimeUtil.validate_str(value)

        # Convert assuming rounding to milliseconds is already done
        datetime_from_str: dt.datetime = dt.datetime.fromisoformat(value[:-1])
        result = DatetimeUtil.from_fields(
            datetime_from_str.year,
            datetime_from_str.month,
            datetime_from_str.day,
            datetime_from_str.hour,
            datetime_from_str.minute,
            datetime_from_str.second,
            millisecond=round(datetime_from_str.microsecond/1000.0)
        )
        return result

    @staticmethod
    def to_fields(value: dt.datetime) -> Tuple[int, int, int, int, int, int, int]:
        """Convert dt.datetime in UTC timezone with millisecond precision to fields."""

        # Validate the datetime first, this will also confirm rounding to milliseconds
        DatetimeUtil.validate_datetime(value)

        # Already round number of milliseconds
        millisecond = value.microsecond // 1000

        # Convert assuming rounding to milliseconds has already been done
        return value.year, value.month, value.day, value.hour, value.minute, value.second, millisecond

    @staticmethod
    def from_fields(
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        *,
        millisecond: Optional[int] = None,
    ) -> dt.datetime:
        """Convert fields with millisecond precision to dt.datetime in UTC timezone."""

        if millisecond is None:
            millisecond = 0

        result = dt.datetime(
            year, month, day, hour, minute, second, microsecond=1000*millisecond, tzinfo=dt.timezone.utc
        )
        return result

    @staticmethod
    def to_iso_int(value: dt.datetime) -> int:
        """Convert dt.datetime in UTC timezone with millisecond precision to int in yyyymmddhhmmssfff format."""

        # Validate the datetime first, this will also confirm rounding to milliseconds
        DatetimeUtil.validate_datetime(value)

        # Convert assuming rounding to milliseconds has already been done
        iso_int = (
                1000_00_00_00_00_00 * value.year +
                1000_00_00_00_00 * value.month +
                1000_00_00_00 * value.day +
                1000_00_00 * value.hour +
                1000_00 * value.minute +
                1000 * value.second +
                value.microsecond // 1000
        )

        return iso_int

    @staticmethod
    def from_iso_int(value: int) -> dt.datetime:
        """Convert int in yyyymmddhhmmssfff format with millisecond precision to dt.datetime in UTC timezone."""

        if value < 10000000000000000:
            raise RuntimeError(f"Datetime {value} is too short for 'yyyymmddhhmmssfff' format.")
        if value > 99999999999999999:
            raise RuntimeError(f"Datetime {value} is too long for 'yyyymmddhhmmssfff' format.")

        year: int = value // 1000_00_00_00_00_00
        value -= year * 1000_00_00_00_00_00
        if year > 9999 or year < 1899:
            raise RuntimeError(f"Invalid year {year} for datetime {value} in 'yyyymmddhhmmssfff' format.")

        month: int = value // 1000_00_00_00_00
        value -= month * 1000_00_00_00_00
        if month > 12 or month < 1:
            raise RuntimeError(f"Invalid month {month} for datetime {value} in 'yyyymmddhhmmssfff' format.")

        day: int = value // 1000_00_00_00
        value -= day * 1000_00_00_00
        if day > 31 or day < 1:
            raise RuntimeError(f"Invalid day {day} for datetime {value} in 'yyyymmddhhmmssfff' format.")

        hour: int = value // 1000_00_00
        value -= hour * 1000_00_00
        if hour > 23 or hour < 0:
            raise RuntimeError(f"Invalid hour {hour} for datetime {value} in 'yyyymmddhhmmssfff' format.")

        minute: int = value // 1000_00
        value -= minute * 1000_00
        if minute > 59 or minute < 0:
            raise RuntimeError(f"Invalid minute {minute} for datetime {value} in 'yyyymmddhhmmssfff' format.")

        second: int = value // 1000
        value -= second * 1000
        if second > 59 or second < 0:
            raise RuntimeError(f"Invalid second {second} for datetime {value} in 'yyyymmddhhmmssfff' format.")

        millisecond: int = value
        if millisecond > 999 or millisecond < 0:
            raise RuntimeError(f"Invalid millisecond {millisecond} for datetime {value} in 'yyyymmddhhmmssfff' format.")

        result = dt.datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
            microsecond=1000 * millisecond,
            tzinfo=dt.timezone.utc,
        )
        return result

    @staticmethod
    def validate_str(value: str) -> None:
        """Validate that datetime string is in ISO-8601 format rounded to milliseconds: 'yyyy-mm-ddThh:mm:ss.fffZ'"""
        if not datetime_pattern.match(value):
            raise RuntimeError(f"Datetime string {value} must be in ISO-8601 format rounded to milliseconds "
                               f"with trailing Z to indicate UTC timezone: 'yyyy-mm-ddThh:mm:ss.fffZ'.")

    @staticmethod
    def validate_datetime(value: dt.datetime) -> None:
        """Validate that datetime object is in UTC time zone and is rounded to milliseconds."""

        # Check timezone
        offset = value.utcoffset()
        if offset is None:
            raise RuntimeError(f"Datetime {value} does not specify timezone. "
                               f"Only UTC timezone is accepted and must be specified explicitly.")
        elif value.utcoffset().total_seconds() != 0:
            raise RuntimeError(f"Datetime {value} is in {value.tzname()} timezone."
                               f"Only UTC timezone is accepted and must be specified explicitly.")

        # Check that datetime is rounded to whole milliseconds
        if value.microsecond % 1000 != 0:
            raise RuntimeError(
                f"Datetime {value} has fractional milliseconds. It must be rounded to"
                f"whole milliseconds using 'DatetimeUtil.round' or similar method."
            )
