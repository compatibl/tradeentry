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
from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.primitive.time_util import TimeUtil
from cl.runtime.records.dataclasses.dataclass_mixin import DataclassMixin
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.storage.data_source_types import TKey
from dataclasses import dataclass
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.records.enum.stub_int_enum import StubIntEnum
from typing import Tuple
from typing import Type
from uuid import UUID

StubDataclassPrimitiveFieldsKey = Tuple[
    Type["StubDataclassPrimitiveFields"],
    str,
    float,
    bool,
    int,
    int,  # Long
    dt.date,
    dt.time,
    dt.datetime,
    UUID,
    bytes,
    StubIntEnum,
    # TODO: Add Tuple when added to the class
]


@dataclass
class StubDataclassPrimitiveFields(DataclassMixin):
    """Stub record whose elements are primitive types."""

    str_field: str = datafield(default="abc")
    """Stub field."""

    float_field: float = datafield(default="1.23")
    """Stub field."""

    bool_field: bool = datafield(default=True)
    """Stub field."""

    int_field: int = datafield(default=123)
    """Stub field."""

    long_field: int = datafield(default=9007199254740991, subtype="long")  # Rename subtype
    """The default is maximum safe signed int for JSON: 2^53 - 1."""
    # TODO: Define maximum safe long in Util class

    date_field: dt.date = datafield(default=DateUtil.from_fields(2003, 5, 1))
    """Stub field."""

    time_field: dt.time = datafield(default=TimeUtil.from_fields(10, 15, 30))
    """Stub field."""

    date_time_field: dt.datetime = datafield(default=DateTimeUtil.from_fields(2003, 5, 1, 10, 15))
    """Stub field."""

    uuid_field: UUID = datafield(default=UUID("1A" * 16))
    """Stub field."""

    bytes_field: bytes = datafield(default=bytes([100, 110, 120]))
    """Stub field."""

    enum_field: StubIntEnum = datafield(default=StubIntEnum.ENUM_VALUE_2)
    """Stub field."""

    base_str_field: str = datafield(default="abc")
    """Stub field."""

    base_float_field: float = datafield(default=1.23)
    """Stub field."""

    base_bool_field: bool = datafield(default=True)
    """Stub field."""

    base_int_field: int = datafield(default=123)
    """Stub field."""

    base_long_field: int = datafield(default=9007199254740991, subtype="long")
    """The default is maximum safe signed int for JSON: 2^53 - 1."""

    base_date_field: dt.date = datafield(default=DateUtil.from_fields(2003, 5, 1))
    """Stub field."""

    base_time_field: dt.time = datafield(default=TimeUtil.from_fields(10, 15, 30))
    """Stub field."""

    base_date_time_field: dt.datetime = datafield(default=DateTimeUtil.from_fields(2003, 5, 1, 10, 15))
    """Stub field."""

    base_uuid_field: UUID = datafield(default=UUID("1A" * 16))
    """Stub field."""

    base_bytes_field: bytes = datafield(default=bytes([100, 110, 120]))
    """Stub field."""

    base_enum_field: StubIntEnum = datafield(default=StubIntEnum.ENUM_VALUE_1)
    """Stub field."""

    base_key_field: TKey = datafield(default=(StubDataclassRecord, "abc", 123))
    """Stub field."""

    def get_key(self) -> StubDataclassPrimitiveFieldsKey:
        return (
            type(self),
            self.str_field,
            self.float_field,
            self.bool_field,
            self.int_field,
            self.long_field,
            self.date_field,
            self.time_field,
            self.date_time_field,
            self.uuid_field,
            self.bytes_field,
            self.enum_field,
        )
