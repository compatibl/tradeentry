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
from cl.runtime.primitive.time_util import TimeUtil


def test_smoke():
    """Smoke test."""

    # Created dates t1-t5 must match this value of string and/or Unix millis
    time_str: str = '10:15:30.500'
    iso_int: int = 101530500

    # Validate
    t1: dt.time = TimeUtil.from_iso_int(iso_int)

    # Create from year, month, day
    t2: dt.time = TimeUtil.from_fields(10, 15, 30, millisecond=500)
    assert t2 == t1

    # Create from string
    t3: dt.time = TimeUtil.from_str(time_str)
    assert t3 == t1

    # Create from dt.time
    t: dt.time = dt.time.fromisoformat('10:15:30.500').replace(tzinfo=dt.timezone.utc)
    t4: dt.time = t
    assert t4 == t1

    # Test conversion to dt.date
    assert t1 == t

    # Test string representation roundtrip
    assert TimeUtil.to_str(t1) == time_str
    t6_str = '10:15:30'
    t6_str_result = '10:15:30.000'
    assert TimeUtil.to_str(TimeUtil.from_str(t6_str)) == t6_str_result

    t7_str = '10:15:30.1'
    t7_str_result = '10:15:30.100'
    assert TimeUtil.to_str(TimeUtil.from_str(t7_str)) == t7_str_result

    t8_str = '10:15:30.12'
    t8_str_result = '10:15:30.120'
    assert TimeUtil.to_str(TimeUtil.from_str(t8_str)) == t8_str_result

    t9_str = '10:15:30.123'
    t9_str_result = '10:15:30.123'
    assert TimeUtil.to_str(TimeUtil.from_str(t9_str)) == t9_str_result

    # Test rounding to the whole millisecond
    t10_str = '10:15:30.1234'
    t10_str_rounded = '10:15:30.123'
    assert TimeUtil.to_str(TimeUtil.from_str(t10_str)) == t10_str_rounded


if __name__ == '__main__':
    pytest.main([__file__])
