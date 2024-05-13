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
from cl.runtime.primitive.date_util import DateUtil


def get_valid_samples() -> List[Tuple[int, str]]:
    """Return a list of valid sample date strings in (iso_int, str) format."""
    return [
        (20030501, "2003-05-01"),
    ]


def get_invalid_string_samples() -> List[str]:
    """Return a list of invalid sample date strings."""
    return [
        "2003-05-01Z",  # Date with timezone
        "20030501Z",  # Date with no spaces and timezone
        "20030501",  # Date with no spaces and no timezone
        "2003.05.01Z",  # Date with dots and timezone
        "2003.05.01",  # Date with dots and no timezone
        "2003/05/01Z",  # Date with slashes and timezone
        "2003/05/01",  # Date with slashes and no timezone
        "2003-05-01T10:15:30Z",  # Datetime with seconds and timezone
        "2003-05-01T10:15:30",  # Datetime with seconds and no timezone
        "2003-05-01T10:15:30.000Z",  # Datetime with milliseconds and timezone
        "2003-05-01T10:15:30.000",  # Datetime with milliseconds and no timezone
        "2003-05-01 10:15:30.000Z",  # Datetime with milliseconds, space instead of T, and timezone
        "2003-05-01 10:15:30.000",  # Datetime with milliseconds, space instead of T, and no timezone
    ]


def get_invalid_iso_int_samples() -> List[int]:
    """Return a list of invalid sample date ISO ints."""
    return [
        2003050,  # Int too short
        18000501,  # Year too far back
        200305010  # Int too long
    ]


def get_invalid_fields_samples() -> List[Tuple[int, int, int]]:
    """Return a list of invalid sample dates in fields format."""
    return [
        (1800, 5, 1),
        (20030, 5, 1),
        (2003, 0, 1),
        (2003, 13, 1),
        (2003, 5, 0),
        (2003, 5, 32),
    ]


def test_to_from_str():
    """Test for to_str, from_str methods."""

    for sample in get_valid_samples():

        from_iso_int_result = DateUtil.from_iso_int(sample[0])
        from_str_result = DateUtil.from_str(sample[1])
        assert from_str_result == from_iso_int_result

        to_str_result = DateUtil.to_str(from_iso_int_result)
        assert to_str_result == sample[1]

    for sample in get_invalid_string_samples():
        with pytest.raises(Exception):
            DateUtil.from_str(sample)


def test_to_from_iso_int():
    """Test for to_iso_int, from_iso_int methods."""

    for sample in get_valid_samples():

        from_str = DateUtil.from_str(sample[1])
        from_iso_int = DateUtil.from_iso_int(sample[0])
        assert from_iso_int == from_str

        iso_int_result = DateUtil.to_iso_int(from_str)
        assert iso_int_result == sample[0]

    for sample in get_invalid_iso_int_samples():
        with pytest.raises(Exception):
            DateUtil.from_iso_int(sample)


def test_to_from_fields():
    """Test for to_fields, from_fields methods."""

    for sample in get_valid_samples():

        date_sample = DateUtil.from_iso_int(sample[0])
        fields_format = DateUtil.to_fields(date_sample)
        date_format = DateUtil.from_fields(*fields_format)
        assert date_format == date_sample

    for sample in get_invalid_fields_samples():
        with pytest.raises(Exception):
            DateUtil.from_fields(sample)


if __name__ == "__main__":
    pytest.main([__file__])
