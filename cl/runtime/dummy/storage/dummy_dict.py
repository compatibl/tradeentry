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

from __future__ import annotations

import uuid
from typing import Any, Dict

import datetime as dt
import numpy as np
import pytz


class DummyDict:
    """Utilities for mock dictionaries."""

    @staticmethod
    def create() -> Dict[str, Any]:
        """Create a mock dictionary with supported primitive data types and containers."""

        result = {
            'str_field': 'abc',
            'bool_field': True,
            'int_field': 123,
            'long_field': 9007199254740991,  # Maximum safe signed int for JS: 2^53 _ 1
            'long_field_str': str(9007199254740991),
            'float_field': 123.456,
          # 'float_numpy_field': np.array([123.456, 789.123]),
            'date_field': dt.date(2003, 4, 21),
            'time_field': dt.time(11, 10, 0),
            'time_field_ms': dt.time(11, 10, 0, 123000),
            'time_field_us': dt.time(11, 10, 0, 123456),
            'datetime_field': dt.datetime(2003, 4, 21, 11, 10, 0, tzinfo=pytz.UTC),
            'datetime_field_ms': dt.datetime(2003, 4, 21, 11, 10, 0, 123000, tzinfo=pytz.UTC),
            'datetime_field_us': dt.datetime(2003, 4, 21, 11, 10, 0, 123456, tzinfo=pytz.UTC),
            'uuid_field': uuid.UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')
        }
        return result
