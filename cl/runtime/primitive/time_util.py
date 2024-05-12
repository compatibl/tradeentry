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
from typing import Optional
from typing import Tuple


class TimeUtil:
    """Util class fro datetime.time."""

    @staticmethod
    def validate(value: dt.time) -> None:
        if value.tzinfo is not None:
            raise Exception(f"Local time of the day {value} must have None time zone.")

        # Check whole milliseconds
        if value.microsecond % 1000 != 0:
            raise RuntimeError(f"Time {value} has fractional milliseconds. " f"Only whole milliseconds are accepted.")

    @staticmethod
    def to_iso_int(value: dt.time) -> int:
        # Round the millisecond
        millisecond: int = round(value.microsecond / 1000.0)

        hour = value.hour
        minute = value.minute
        second = value.second

        # If millisecond is not specified, assume 0
        if millisecond is None:
            millisecond = 0

        # Convert to dt.time represented in hhmmssfff format
        iso_int: int = 10_000_000 * hour + 100_000 * minute + 1000 * second + millisecond
        return iso_int

    @staticmethod
    def from_iso_int(iso_int: int) -> Any:
        hour, minute, second, millisecond = TimeUtil._iso_int_to_fields(iso_int)

        # The resulting dt.time must not have a timezone
        result: dt.time = dt.time(hour, minute, second, 1000 * millisecond, dt.timezone.utc)
        return result

    @staticmethod
    def to_str(value: dt.time) -> str:
        # Convert to string in ISO format without timezone, with
        # 3 digits after decimal points for seconds, irrespective of
        # how many digits are actually required.
        result_to_microseconds: str = value.strftime("%H:%M:%S.%f")
        result: str = result_to_microseconds[:-3]
        return result

    @staticmethod
    def from_str(value_str: str) -> Any:
        if not value_str[-1].isdigit():
            raise Exception(f"String {value_str} passed to from_str(...) method " f"must not include timezone.")

        # Convert to datetime and set UTC timezone
        if "." in value_str:
            # Has milliseconds
            t = dt.datetime.strptime(value_str, "%H:%M:%S.%f").time()
        else:
            # Does not have milliseconds
            t = dt.datetime.strptime(value_str, "%H:%M:%S").time()

        # Round the result to whole milliseconds
        rounded_microsecond: int = round(t.microsecond / 1000.0) * 1000
        rounded_time: dt.time = dt.time(t.hour, t.minute, t.second, rounded_microsecond, dt.timezone.utc)
        return rounded_time

    @staticmethod
    def from_fields(
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        *,
        millisecond: Optional[int] = None,
    ) -> dt.time:
        """
        Create dt.time from fields in UTC timezone with one millisecond precision,
        milliseconds is a named parameter to avoid the risk of passing microseconds instead.
        """

        if millisecond is None:
            millisecond = 0

        result = dt.time(hour, minute, second, microsecond=1000 * millisecond, tzinfo=dt.timezone.utc)
        return result

    @staticmethod
    def _iso_int_to_fields(value: int) -> Tuple[int, int, int, int]:
        """
        Convert Time stored as int in ISO hhmmssfff format to
        the tuple (hour, minute, second, millisecond).

        This method does not perform validation of its argument.
        """

        hour: int = value // 10_000_000
        value -= hour * 10_000_000
        minute: int = value // 100_000
        value -= minute * 100_000
        second: int = value // 1_000
        value -= second * 1_000
        millisecond: int = value

        return hour, minute, second, millisecond
