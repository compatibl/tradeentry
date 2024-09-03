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
from cl.runtime.storage.data_source_types import TDataDict
from uuid import UUID


class StubDictUtil:
    """Utilities for mock dictionaries."""

    @staticmethod
    def create_primitive() -> TDataDict:
        """Create a mock dictionary whose fields include all supported primitive types."""

        result = {
            "str_field": "abc",
            "float_field": 123.456,
            "bool_field": True,
            "int_field": 123,
            "long_field": 9007199254740991,  # Maximum safe signed int for JSON: 2^53 - 1
            "long_field_str": str(9007199254740991),  # Maximum safe signed int for JSON: 2^53 - 1
            "date_field": dt.date(2003, 4, 21),
            "time_field": dt.time(11, 10, 0),
            "time_field_ms": dt.time(11, 10, 0, 123000),
            "time_field_us": dt.time(11, 10, 0, 123456),
            "datetime_field": dt.datetime(2003, 4, 21, 11, 10, 0, tzinfo=dt.timezone.utc),
            "datetime_field_ms": dt.datetime(2003, 4, 21, 11, 10, 0, 123000, tzinfo=dt.timezone.utc),
            "datetime_field_us": dt.datetime(2003, 4, 21, 11, 10, 0, 123456, tzinfo=dt.timezone.utc),
            "uuid_field": UUID("1A" * 16),
            "bytes": b"abc",
        }
        return result
