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
import pytest
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from typing import List
from typing import Tuple
from zoneinfo import ZoneInfo


def get_valid_samples() -> List[Tuple[int, str]]:
    """Return a list of valid sample date strings in (iso_int, str) format."""
    return [(20030501101530000, "2003-05-01T10:15:30.000Z"), (20030501101530500, "2003-05-01T10:15:30.500Z")]


def get_invalid_datetime_samples() -> List[dt.datetime]:
    """Return a list of invalid sample datetime strings."""

    non_utc_timezone = ZoneInfo("America/New_York")

    return [
        dt.datetime(2003, 5, 1, 10, 15, 30, microsecond=1234, tzinfo=dt.timezone.utc),  # Not rounded
        dt.datetime(2003, 5, 1, 10, 15, 30),  # No timezone
        dt.datetime(2003, 5, 1, 10, 15, 30, tzinfo=non_utc_timezone),  # Non-UTC timezone
    ]


def get_invalid_string_samples() -> List[str]:
    """Return a list of invalid sample datetime strings."""
    return [
        "2003-05-01",  # Date only with no timezone
        "2003-05-01Z",  # Date only
        "2003-05-01 10:15:30.000Z",  # Space instead of T
        "2003-05-01T10:15Z",  # No seconds
        "2003-05-01T10:15:30Z",  # No milliseconds
        "2003-05-01T10:15:30.000",  # No timezone
    ]


def get_invalid_iso_int_samples() -> List[int]:
    """Return a list of invalid sample datetime ISO ints."""
    return [
        20030501,  # Date only
        200305011015,  # No seconds
        20030501101530,  # No milliseconds
        2003050110153000,  # Int too short
        180005011015300000,  # Year too far back
        200305011015300000,  # Int too long
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
        (2003, 5, 1, 10, 15, 30, -1),
        (2003, 5, 1, 10, 15, 30, 1000),
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


def test_now():
    """Test rounding current time to whole milliseconds."""

    for _ in range(1000):
        # Datetime before rounded down to 1ms per UUIDv7 RFC-9562 standard
        datetime_before = DatetimeUtil.floor(dt.datetime.now(dt.timezone.utc))

        # Datetime from ordered UUID before rounded down to 1ms per UUIDv7 RFC-9562 standard
        from_ordered_uuid_before = OrderedUuid.datetime_of(OrderedUuid.create_one())
        now = DatetimeUtil.now()

        # Datetime from ordered UUID after rounded down to 1ms per UUIDv7 RFC-9562 standard
        from_ordered_uuid_after = OrderedUuid.datetime_of(OrderedUuid.create_one())

        # Datetime after rounded up to 1ms per UUIDv7 RFC-9562 standard
        datetime_after = DatetimeUtil.ceil(dt.datetime.now(dt.timezone.utc))

        # Check that DatetimeUtil.now is consistent with the timestamp of OrderedUid.create_one()
        assert from_ordered_uuid_before <= now
        assert now <= from_ordered_uuid_after

        # Check that the timestamp of OrderedUid.create_one() is consistent with native dt.datetime.now up to tolerance
        tolerance_before_ms = 0
        tolerance_after_ms = 1
        assert datetime_before - dt.timedelta(milliseconds=tolerance_before_ms) <= from_ordered_uuid_before
        assert from_ordered_uuid_after <= datetime_after + dt.timedelta(milliseconds=tolerance_after_ms)

        # Check that timestamp is rounded to 1ms and has UTC timezone
        assert now.microsecond % 1000 == 0
        assert now.tzinfo == dt.timezone.utc


def test_rounding():
    """Test rounding to whole milliseconds."""

    for sample in get_rounding_samples():
        value = sample[0]
        correct_rounded_value = sample[1]
        rounded = DatetimeUtil.round(value)
        rounded_down = DatetimeUtil.floor(value)
        rounded_up = DatetimeUtil.ceil(value)

        # Check that rounded value matches expected
        assert rounded == correct_rounded_value

        # Check rounded down and up values
        if value.microsecond % 1000 == 0:
            # Sample is already rounded to milliseconds
            assert rounded_down == rounded
            assert rounded_up == rounded
        else:
            # Sample not rounded to milliseconds

            # Check rounding direction
            assert rounded_down < value
            assert rounded_up > value

            # Check rounding values
            microsecond_down = 1000 * (value.microsecond // 1000)
            assert rounded_down == value.replace(microsecond=microsecond_down)

            microsecond_up = 1000 * (value.microsecond // 1000 + 1)
            if microsecond_up == 1_000_000:
                assert rounded_up == value.replace(microsecond=0) + dt.timedelta(seconds=1)
            else:
                assert rounded_up == value.replace(microsecond=1000 * (value.microsecond // 1000 + 1))


def test_to_from_str():
    """Test for to_str, from_str methods."""

    for sample in get_valid_samples():
        from_iso_int_result = DatetimeUtil.from_iso_int(sample[0])
        from_str_result = DatetimeUtil.from_str(sample[1])
        assert from_str_result == from_iso_int_result

        to_str_result = DatetimeUtil.to_str(from_iso_int_result)
        assert to_str_result == sample[1]

    for sample in get_invalid_datetime_samples():
        with pytest.raises(Exception):
            DatetimeUtil.to_str(sample)

    for sample in get_invalid_string_samples():
        with pytest.raises(Exception):
            DatetimeUtil.from_str(sample)


def test_to_from_iso_int():
    """Test for to_iso_int, from_iso_int methods."""

    for sample in get_valid_samples():
        from_str = DatetimeUtil.from_str(sample[1])
        from_iso_int = DatetimeUtil.from_iso_int(sample[0])
        assert from_iso_int == from_str

        iso_int_result = DatetimeUtil.to_iso_int(from_str)
        assert iso_int_result == sample[0]

    for sample in get_invalid_iso_int_samples():
        with pytest.raises(Exception):
            DatetimeUtil.from_iso_int(sample)


def test_to_from_fields():
    """Test for to_fields, from_fields methods."""

    for sample in get_valid_samples():
        datetime_sample = DatetimeUtil.from_iso_int(sample[0])
        fields_format = DatetimeUtil.to_fields(datetime_sample)

        positional_args = fields_format[:-1]
        datetime_format = DatetimeUtil.from_fields(*positional_args, millisecond=fields_format[-1])
        assert datetime_format == datetime_sample

    for sample in get_invalid_fields_samples():
        with pytest.raises(Exception):
            DatetimeUtil.from_fields(sample)


if __name__ == "__main__":
    pytest.main([__file__])
