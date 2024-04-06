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
from cl.runtime.primitive.date_time_util import DateTimeUtil


def test_smoke():
    """Smoke test"""

    # Created dates t1-t5 must match this value of string and/or Unix millis
    date_str: str = '2003-05-01T10:15:30.500'
    iso_int: int = 20030501101530500

    # Validation
    from_iso_int: dt.datetime = DateTimeUtil.from_iso_int(iso_int)

    # Create from year, month, day
    d2: dt.datetime = DateTimeUtil.from_fields(2003, 5, 1, 10, 15, 30, millisecond=500)
    assert d2 == from_iso_int

    # Create from string
    d3: dt.datetime = DateTimeUtil.from_str(date_str)
    assert d3 == from_iso_int

    # Create from dt.date
    d: dt.datetime = DateTimeUtil.from_str(date_str)
    d4: dt.datetime = d
    assert d4 == from_iso_int

    # Test conversion to dt.datetime
    assert from_iso_int == d

    # Test string representation roundtrip
    assert DateTimeUtil.to_str(from_iso_int) == date_str


if __name__ == '__main__':
    pytest.main([__file__])
