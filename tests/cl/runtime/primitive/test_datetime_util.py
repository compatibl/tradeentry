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
from typing import List, Tuple
from zoneinfo import ZoneInfo

import pytest
from cl.runtime.primitive.date_time_util import DateTimeUtil


def get_valid_samples() -> List[Tuple[int, str]]:
    """Return a list of valid sample date strings in (iso_int, str) format."""
    return [
        (20030501101530000, "2003-05-01T10:15:30.000Z"),
        (20030501101530500, "2003-05-01T10:15:30.500Z")
    ]


def get_invalid_datetime_samples() -> List[dt.datetime]:
    """Return a list of invalid sample datetime strings."""

    non_utc_timezone = ZoneInfo('America/New_York')

    return [
        dt.datetime(2003, 5, 1, 10, 15, 30),  # No timezone
        dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=1234, tzinfo=dt.timezone.utc),  # Not rounded
        dt.datetime(2003, 5, 1, 10, 15, 30, tzinfo=non_utc_timezone)
    ]


def get_invalid_string_samples() -> List[str]:
    """Return a list of invalid sample datetime strings."""
    return [
        "2003-05-01",
        "2003-05-01Z",
        "2003-05-01 10:15:30.000Z",
        "2003-05-01T10:15Z",
        "2003-05-01T10:15:30Z",
        "2003-05-01T10:15:30.000",
    ]


def get_invalid_iso_int_samples() -> List[int]:
    """Return a list of invalid sample datetime ISO ints."""
    return [
        18000501,
        20030501,
        200305011015,
        20030501101530,
        2003050110153000,
        200305011015300000
    ]


def get_invalid_fields_samples() -> List[Tuple[int, int, int, int, int, int, int]]:
    """Return a list of invalid sample datetimes in fields format."""
    return [
        (1800, 5, 1, 10, 15, 30, 500),
        (20030, 5, 1, 10, 15, 30, 500),
        (2003, 0, 1, 10, 15, 30, 500),
        (2003, 13, 1, 10, 15, 30, 500),
        (2003, 5, 0, 10, 15, 30, 500),
        (2003, 5, 32, 10, 15, 30, 500),
        (2003, 5, 1, -1, 15, 30, 500),
        (2003, 5, 1, 24, 15, 30, 500),
        (2003, 5, 1, 10, -1, 30, 500),
        (2003, 5, 1, 10, 60, 30, 500),
        (2003, 5, 1, 10, 15, -1, 500),
        (2003, 5, 1, 10, 15, 60, 500),
        (1800, 5, 1, 10, 15, 30, -1),
        (1800, 5, 1, 10, 15, 30, 1000),
    ]


def get_rounding_samples() -> List[Tuple[dt.datetime, dt.datetime]]:
    """Return a list of datetime objects for testing rounding."""

    return [
        (
            dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=0, tzinfo=dt.timezone.utc),
            dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=0, tzinfo=dt.timezone.utc),
        ),
        (
            dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=5000, tzinfo=dt.timezone.utc),
            dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=5000, tzinfo=dt.timezone.utc),
        ),
        (
            dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=1234, tzinfo=dt.timezone.utc),
            dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=1000, tzinfo=dt.timezone.utc),
        ),
        (
            dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=999499, tzinfo=dt.timezone.utc),
            dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=999000, tzinfo=dt.timezone.utc),
        ),
        (
            dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=999501, tzinfo=dt.timezone.utc),
            dt.datetime(2003, 5, 1, 10, 15, 31, microsecond=0, tzinfo=dt.timezone.utc),
        ),
    ]


def test_to_from_str():
    """Test for to_str, from_str methods."""

    for sample in get_valid_samples():

        from_iso_int_result = DateTimeUtil.from_iso_int(sample[0])
        from_str_result = DateTimeUtil.from_str(sample[1])
        assert from_str_result == from_iso_int_result

        to_str_result = DateTimeUtil.to_str(from_iso_int_result)
        assert to_str_result == sample[1]

    for sample in get_invalid_datetime_samples():
        with pytest.raises(Exception):
            DateTimeUtil.to_str(sample)

    for sample in get_invalid_string_samples():
        with pytest.raises(Exception):
            DateTimeUtil.from_str(sample)


def test_to_from_iso_int():
    """Test for to_iso_int, from_iso_int methods."""

    for sample in get_valid_samples():

        from_str = DateTimeUtil.from_str(sample[1])
        from_iso_int = DateTimeUtil.from_iso_int(sample[0])
        assert from_iso_int == from_str

        iso_int_result = DateTimeUtil.to_iso_int(from_str)
        assert iso_int_result == sample[0]

    for sample in get_invalid_iso_int_samples():
        with pytest.raises(Exception):
            DateTimeUtil.from_iso_int(sample)


def test_to_from_fields():
    """Test for to_fields, from_fields methods."""

    for sample in get_valid_samples():

        datetime_sample = DateTimeUtil.from_iso_int(sample[0])
        fields_format = DateTimeUtil.to_fields(datetime_sample)

        positional_args = fields_format[:-1]
        datetime_format = DateTimeUtil.from_fields(*positional_args, millisecond=fields_format[-1])
        assert datetime_format == datetime_sample

    for sample in get_invalid_fields_samples():
        with pytest.raises(Exception):
            DateTimeUtil.from_fields(sample)


def test_round():
    """Test rounding to millisecond."""

    for sample in get_rounding_samples():

        rounded = DateTimeUtil.round(sample[0])
        assert rounded == sample[1]


if __name__ == "__main__":
    pytest.main([__file__])
