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

import pytest
import datetime as dt
from typing import Iterable
from uuid import UUID
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.primitive.timestamp import Timestamp
from cl.runtime.testing.regression_guard import RegressionGuard


def is_ordered(values: Iterable[str]):
    if not hasattr(values, "__len__") or not hasattr(values, "__getitem__"):
        values = list(values)
    return all(values[i] < values[i + 1] for i in range(len(values) - 1))


def test_create():
    """Test Timestamp.create_one method."""

    result_1 = [Timestamp.create() for _ in range(10)]
    result_2 = [Timestamp.create() for _ in range(10)]
    result = result_1 + result_2
    assert is_ordered(result_1)
    assert is_ordered(result_1)
    assert is_ordered(result)


def test_create_many():
    """Test Timestamp.create_one method."""

    result_1 = Timestamp.create_many(10)
    result_2 = Timestamp.create_many(10)
    result = result_1 + result_2
    assert is_ordered(result_1)
    assert is_ordered(result_1)
    assert is_ordered(result)


def test_time_ordering():
    """Test Timestamp.to_datetime method."""

    # Allow for 3ms tolerance between timer reading of UUIDv7 generator and datetime.now method
    tolerance_ms = 3
    for _ in range(1000):
        # Datetime before rounded down to 1ms per UUIDv7 RFC-9562 standard
        datetime_before = DatetimeUtil.floor(dt.datetime.now(dt.timezone.utc))

        # Get result
        datetime_result = Timestamp.to_datetime(Timestamp.create())

        # Datetime after rounded up to 1ms per UUIDv7 RFC-9562 standard
        datetime_after = DatetimeUtil.ceil(dt.datetime.now(dt.timezone.utc))

        # Check that timestamp is within the expected range, allowing for tolerance in timer reading
        assert datetime_before - dt.timedelta(milliseconds=tolerance_ms) <= datetime_result
        assert datetime_result <= datetime_after + dt.timedelta(milliseconds=tolerance_ms)

        # Check that timestamp is rounded to 1ms and has UTC timezone
        assert datetime_result.microsecond % 1000 == 0
        assert datetime_result.tzinfo == dt.timezone.utc


def test_validate():
    """Test Timestamp.validate method."""
    guard = RegressionGuard()
    try:
        Timestamp.validate("123")
    except Exception as e:
        guard.write(e)
    try:
        Timestamp.validate("2024-09-25T23:00:29.307Z-7030856bcce0da7fdbdf")
    except Exception as e:
        guard.write(e)
    RegressionGuard.verify(guard)


if __name__ == "__main__":
    pytest.main([__file__])
