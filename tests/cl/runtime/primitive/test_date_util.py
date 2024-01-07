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
from dateutil.relativedelta import relativedelta
from cl.runtime.primitive.date_util import DateUtil


def test_smoke():
    """Smoke test"""

    # Created dates t1-t5 must match this value of string and/or Unix millis
    date_str: str = '2003-05-01'
    iso_int: int = 20030501

    # Validation
    from_iso_int: dt.date = DateUtil.from_iso_int(iso_int)

    # Create from year, month, day
    d2: dt.date = DateUtil.from_fields(2003, 5, 1)
    assert d2 == from_iso_int

    # Create from string
    d3: dt.date = DateUtil.from_str(date_str)
    assert d3 == from_iso_int

    # Create from dt.date
    d: dt.date = dt.date.fromisoformat(date_str)
    d4: dt.date = d
    assert d4 == from_iso_int

    # Test conversion to dt.date
    assert from_iso_int == d

    # Test string representation roundtrip
    assert DateUtil.to_str(from_iso_int) == date_str


def test_add_relative_delta():
    """Test + operator with dateutil relativedelta."""

    date_1 = DateUtil.from_fields(2003, 5, 1)
    rel_date_1 = date_1 + relativedelta(days=45)
    assert (rel_date_1.year, rel_date_1.month, rel_date_1.day) == (2003, 6, 15)


if __name__ == '__main__':
    pytest.main([__file__])
