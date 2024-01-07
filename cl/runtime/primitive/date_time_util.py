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
from typing import Any, Optional, Tuple


class DateTimeUtil:
    """Util class for datetime.datetime."""

    @staticmethod
    def validate(value: dt.datetime) -> None:
        """Checks if the value is in the UTC time zone and is accurate to milliseconds."""

        # Check timezone
        offset = value.utcoffset()
        if offset is not None and value.utcoffset().total_seconds() != 0:
            raise RuntimeError(f'Datetime {value} is not in UTC timezone.')

        # Check whole milliseconds
        if value.microsecond % 1000 != 0:
            raise RuntimeError(
                f'Datetime {value} has fractional milliseconds. ' f'Only whole milliseconds are accepted.'
            )

    @staticmethod
    def to_iso_int(value: dt.datetime) -> int:
        iso_int = (
            1000_00_00_00_00_00 * value.year
            + 1000_00_00_00_00 * value.month
            + 1000_00_00_00 * value.day
            + 1000_00_00 * value.hour
            + 1000_00 * value.minute
            + 1000 * value.second
            + value.microsecond // 1000
        )

        return iso_int

    @staticmethod
    def from_iso_int(iso_int: int) -> Any:
        (
            year,
            month,
            day,
            hour,
            minute,
            second,
            millisecond,
        ) = DateTimeUtil._to_fields_lenient(iso_int)

        # This will also validate the date
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
    def to_str(value: dt.datetime) -> str:
        result: str = value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        return result

    @staticmethod
    def from_str(value_str: str) -> Any:
        if value_str.endswith('Z'):
            raise Exception(
                f'String {value_str} passed to dt.datetime ctor must not end with capital Z that '
                f'indicates UTC timezone because dt.datetime is always specified in UTC, and its'
                f'standard string representation does not include timezone (UTC is always used).'
            )

            # Convert from string in yyyy-mm-ddThh:mm:ss.fff format
        datetime_without_tz: dt.datetime = dt.datetime.fromisoformat(value_str)
        date_from_str = DateTimeUtil.from_fields(
            datetime_without_tz.year,
            datetime_without_tz.month,
            datetime_without_tz.day,
            datetime_without_tz.hour,
            datetime_without_tz.minute,
            datetime_without_tz.second,
            millisecond=round(datetime_without_tz.microsecond / 1000.0),
        )
        return date_from_str

    @staticmethod
    def _to_fields_lenient(value: int) -> Tuple[int, int, int, int, int, int, int]:
        """
        Convert dt.datetime represented as int in yyyymmddhhmmssfff format to
        the tuple (year, month, day, hour, minute, second, millisecond).

        This method does not perform validation of its argument.
        """

        year: int = value // 1000_00_00_00_00_00
        value -= year * 1000_00_00_00_00_00
        month: int = value // 1000_00_00_00_00
        value -= month * 1000_00_00_00_00
        day: int = value // 1000_00_00_00
        value -= day * 1000_00_00_00
        hour: int = value // 1000_00_00
        value -= hour * 1000_00_00
        minute: int = value // 1000_00
        value -= minute * 1000_00
        second: int = value // 1000
        value -= second * 1000
        millisecond: int = value

        return year, month, day, hour, minute, second, millisecond

    @staticmethod
    def from_fields(
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        *,
        millisecond: Optional[int] = None,
    ) -> dt.datetime:
        """Create datetime from fields in UTC timezone to millisecond precision."""

        if millisecond is None:
            millisecond = 0

        result = dt.datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
            microsecond=1000*millisecond,
            tzinfo=dt.timezone.utc
        )
        return result
