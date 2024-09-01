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
import uuid
import datetime as dt
from typing import List

from cl.runtime.primitive.datetime_util import DatetimeUtil

from cl.runtime.primitive.uuid_util import UuidUtil


def is_ordered(values: List[uuid.UUID]):
    return all(values[i] < values[i+1] for i in range(len(values) - 1))


def test_create_one():
    """Test UuidUtil.create_one method."""

    result_1 = [UuidUtil.create_one() for _ in range(10)]
    result_2 = [UuidUtil.create_one() for _ in range(10)]
    result = result_1 + result_2
    assert is_ordered(result)


def test_datetime_of():
    """Test UuidUtil.datetime_of method."""

    # Datetime before rounded down to 1ms per UUIDv7 RFC-9562 standard
    datetime_before = DatetimeUtil.floor(dt.datetime.now(dt.timezone.utc))

    datetime_result = UuidUtil.datetime_of(UuidUtil.create_one())

    # Datetime after rounded up to 1ms per UUIDv7 RFC-9562 standard
    datetime_after = DatetimeUtil.ceil(dt.datetime.now(dt.timezone.utc))

    # Check that timestamp is within the expected range
    assert datetime_before <= datetime_result
    assert datetime_result <= datetime_after

    # Check that timestamp is rounded to 1ms and has UTC timezone
    assert datetime_result.microsecond % 1000 == 0
    assert datetime_result.tzinfo == dt.timezone.utc


if __name__ == "__main__":
    pytest.main([__file__])
