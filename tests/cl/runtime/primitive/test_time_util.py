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
from cl.runtime.primitive.time_util import TimeUtil


def get_valid_samples() -> List[Tuple[int, str]]:
    """Return a list of valid sample date strings in (iso_int, str) format."""
    return [
        (101530000, "10:15:30.000"),
        (101530500, "10:15:30.500")
    ]


def get_invalid_time_samples() -> List[dt.time]:
    """Return a list of invalid sample time strings."""

    non_utc_timezone = ZoneInfo('America/New_York')

    return [
        dt.time(10, 15, 30, microsecond=1234),  # Not rounded
        dt.time(10, 15, 30, tzinfo=dt.timezone.utc),  # UTC timezone
        dt.time(10, 15, 30, tzinfo=non_utc_timezone)  # Non-UTC timezone
    ]


def get_invalid_string_samples() -> List[str]:
    """Return a list of invalid sample time strings."""
    return [
        "10:15Z", # No seconds
        "10:15:30Z",  # No milliseconds
        "10:15:30.000Z",  # Specifies timezone
    ]


def get_invalid_iso_int_samples() -> List[int]:
    """Return a list of invalid sample time ISO ints."""
    return [
        -1,  # Too small
        1015,  # No seconds
        101530,  # No milliseconds
        10153000,  # Int too short
        1015300000  # Int too long
    ]


def get_invalid_fields_samples() -> List[Tuple[int, int, int, int]]:
    """Return a list of invalid sample times in fields format."""
    return [
        (-1, 15, 30, 500),
        (24, 15, 30, 500),
        (10, -1, 30, 500),
        (10, 60, 30, 500),
        (10, 15, -1, 500),
        (10, 15, 60, 500),
        (10, 15, 30, -1),
        (10, 15, 30, 1000),
    ]


def get_rounding_samples() -> List[Tuple[dt.time, dt.time]]:
    """Return a list of time objects for testing rounding."""

    return [
        (
            dt.time(10, 15, 30, microsecond=0),
            dt.time(10, 15, 30, microsecond=0),
        ),
        (
            dt.time(10, 15, 30, microsecond=5000),
            dt.time(10, 15, 30, microsecond=5000),
        ),
        (
            dt.time(10, 15, 30, microsecond=1234),
            dt.time(10, 15, 30, microsecond=1000),
        ),
        (
            dt.time(10, 15, 30, microsecond=999499),
            dt.time(10, 15, 30, microsecond=999000),
        ),
        (
            dt.time(10, 15, 30, microsecond=999501),
            dt.time(10, 15, 31, microsecond=0),
        ),
    ]


def test_to_from_str():
    """Test for to_str, from_str methods."""

    for sample in get_valid_samples():

        from_iso_int_result = TimeUtil.from_iso_int(sample[0])
        from_str_result = TimeUtil.from_str(sample[1])
        assert from_str_result == from_iso_int_result

        to_str_result = TimeUtil.to_str(from_iso_int_result)
        assert to_str_result == sample[1]

    for sample in get_invalid_time_samples():
        with pytest.raises(Exception):
            TimeUtil.to_str(sample)

    for sample in get_invalid_string_samples():
        with pytest.raises(Exception):
            TimeUtil.from_str(sample)


def test_to_from_iso_int():
    """Test for to_iso_int, from_iso_int methods."""

    for sample in get_valid_samples():

        from_str = TimeUtil.from_str(sample[1])
        from_iso_int = TimeUtil.from_iso_int(sample[0])
        assert from_iso_int == from_str

        iso_int_result = TimeUtil.to_iso_int(from_str)
        assert iso_int_result == sample[0]

    for sample in get_invalid_iso_int_samples():
        with pytest.raises(Exception):
            TimeUtil.from_iso_int(sample)


def test_to_from_fields():
    """Test for to_fields, from_fields methods."""

    for sample in get_valid_samples():

        time_sample = TimeUtil.from_iso_int(sample[0])
        fields_format = TimeUtil.to_fields(time_sample)

        positional_args = fields_format[:-1]
        time_format = TimeUtil.from_fields(*positional_args, millisecond=fields_format[-1])
        assert time_format == time_sample

    for sample in get_invalid_fields_samples():
        with pytest.raises(Exception):
            TimeUtil.from_fields(sample)


def test_round():
    """Test rounding to millisecond."""

    for sample in get_rounding_samples():

        rounded = TimeUtil.round(sample[0])
        assert rounded == sample[1]


if __name__ == "__main__":
    pytest.main([__file__])
