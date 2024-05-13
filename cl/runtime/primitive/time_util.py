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

# Compile the regex pattern for time in ISO-8601 format hh:mm:ss.fff without timezone
time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3}$")


class TimeUtil:
    """Utility class for dt.time."""

    @staticmethod
    def round(value: dt.time) -> dt.time:
        """Round to whole milliseconds (the argument must already be in UTC timezone)."""
        
        # Check that timezone is not set
        if value.tzinfo is not None:
            raise RuntimeError(f"Time {value} is not accepted because it specifies timezone {value.tzname()}. "
                               f"Time must have tzinfo=None which is the default value.")

        fractional_milliseconds_float = 1000.0 * value.second + value.microsecond / 1000.0
        rounded_microseconds = round(fractional_milliseconds_float)

        second: int = rounded_microseconds // 1_000
        rounded_microseconds -= second * 1_000
        if second > 59 or second < 0:
            raise RuntimeError(f"Invalid second {second} for datetime {value} after rounding.")

        millisecond: int = rounded_microseconds
        if millisecond > 999 or millisecond < 0:
            raise RuntimeError(f"Invalid millisecond {millisecond} for datetime {value} after rounding.")

        result = dt.time(value.hour,
                         value.minute,
                         second,  # New value from rounding
                         1_000 * millisecond,  # New value from rounding
                         )
        return result

    @staticmethod
    def to_str(value: dt.time) -> str:
        """Convert to string in ISO-8601 format rounded to milliseconds: 'hh:mm:ss.fff'"""

        # Validate timezone and rounding to milliseconds
        TimeUtil.validate_time(value)

        # Already round number of milliseconds
        millisecond = value.microsecond // 1000

        # Convert to string
        result = f"{value.hour:02}:{value.minute:02}:{value.second:02}.{millisecond:03}"
        return result

    @staticmethod
    def from_str(value: str) -> dt.time:
        """Convert from string in ISO-8601 format rounded to milliseconds: 'hh:mm:ss.fff'"""

        # Validate string format and that tzinfo is None
        TimeUtil.validate_str(value)

        # Convert assuming rounding to milliseconds is already done
        time_from_str: dt.time = dt.time.fromisoformat(value)
        result = TimeUtil.from_fields(
            time_from_str.hour,
            time_from_str.minute,
            time_from_str.second,
            millisecond=round(time_from_str.microsecond/1000.0)
        )
        return result

    @staticmethod
    def to_fields(value: dt.time) -> Tuple[int, int, int, int]:
        """Convert dt.time in UTC timezone with millisecond precision to fields."""

        # Validate the time first, this will also confirm rounding to milliseconds
        TimeUtil.validate_time(value)

        # Already round number of milliseconds
        millisecond = value.microsecond // 1000

        # Convert assuming rounding to milliseconds has already been done
        return value.hour, value.minute, value.second, millisecond

    @staticmethod
    def from_fields(
        hour: int,
        minute: int,
        second: int,
        *,
        millisecond: Optional[int] = None,
    ) -> dt.time:
        """Convert fields with millisecond precision to dt.time."""

        if millisecond is None:
            millisecond = 0

        result = dt.time(hour, minute, second, microsecond=1000*millisecond)
        return result

    @staticmethod
    def to_iso_int(value: dt.time) -> int:
        """Convert dt.time with millisecond precision to int in hhmmssfff format."""

        # Validate the time first, this will also confirm rounding to milliseconds
        TimeUtil.validate_time(value)

        # Convert assuming rounding to milliseconds has already been done
        iso_int = (1000_00_00 * value.hour +
                   1000_00 * value.minute +
                   1000 * value.second +
                   value.microsecond // 1000
        )

        return iso_int

    @staticmethod
    def from_iso_int(value: int) -> dt.time:
        """Convert int in hhmmssfff format with millisecond precision to dt.time."""

        if value < 100000000:
            raise RuntimeError(f"Time {value} is too short for 'hhmmssfff' format.")
        if value > 999999999:
            raise RuntimeError(f"Time {value} is too long for 'hhmmssfff' format.")

        hour: int = value // 1000_00_00
        value -= hour * 1000_00_00
        if hour > 23 or hour < 0:
            raise RuntimeError(f"Invalid hour {hour} for time {value} in 'hhmmssfff' format.")

        minute: int = value // 1000_00
        value -= minute * 1000_00
        if minute > 59 or minute < 0:
            raise RuntimeError(f"Invalid minute {minute} for time {value} in 'hhmmssfff' format.")

        second: int = value // 1000
        value -= second * 1000
        if second > 59 or second < 0:
            raise RuntimeError(f"Invalid second {second} for time {value} in 'hhmmssfff' format.")

        millisecond: int = value
        if millisecond > 999 or millisecond < 0:
            raise RuntimeError(f"Invalid millisecond {millisecond} for time {value} in 'hhmmssfff' format.")

        result = dt.time(
            hour,
            minute,
            second,
            microsecond=1000 * millisecond
        )
        return result

    @staticmethod
    def validate_str(value: str) -> None:
        """Validate that time string is in ISO-8601 format rounded to milliseconds: 'hh:mm:ss.fff'"""
        if not time_pattern.match(value):
            raise RuntimeError(f"Time string {value} must be in ISO-8601 format rounded to milliseconds "
                               f"without timezone: 'hh:mm:ss.fff'.")

    @staticmethod
    def validate_time(value: dt.time) -> None:
        """Validate that time object does not have time zone and is rounded to milliseconds."""

        # Check that timezone is not set
        if value.tzinfo is not None:
            raise RuntimeError(f"Time {value} is not accepted because it specifies timezone {value.tzname()}. "
                               f"Time must have tzinfo=None which is the default value.")

        # Check that time is rounded to whole milliseconds
        if value.microsecond % 1000 != 0:
            raise RuntimeError(
                f"Time {value} has fractional milliseconds. It must be rounded to"
                f"whole milliseconds using 'TimeUtil.round' or similar method."
            )
