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
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.primitive.time_util import TimeUtil
from cl.runtime.records.dataclasses.dataclass_mixin import DataclassMixin
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.storage.data_source_types import TKey
from dataclasses import dataclass
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.records.dataclasses.stub_dataclass_primitive_fields_key import StubDataclassPrimitiveFieldsKey
from stubs.cl.runtime.records.enum.stub_int_enum import StubIntEnum
from typing import Tuple
from typing import Type
from uuid import UUID


@dataclass
class StubDataclassPrimitiveFields(DataclassMixin):
    """Stub record whose elements are primitive types."""

    key_str_field: str = datafield(default="abc")
    """Stub field."""

    key_float_field: float = datafield(default=1.23)
    """Stub field."""

    key_bool_field: bool = datafield(default=True)
    """Stub field."""

    key_int_field: int = datafield(default=123)
    """Stub field."""

    key_long_field: int = datafield(default=9007199254740991, subtype="long")  # Rename subtype
    """The default is maximum safe signed int for JSON: 2^53 - 1."""
    # TODO: Define maximum safe long in Util class

    key_date_field: dt.date = datafield(default=DateUtil.from_fields(2003, 5, 1))
    """Stub field."""

    key_time_field: dt.time = datafield(default=TimeUtil.from_fields(10, 15, 30))
    """Stub field."""

    key_date_time_field: dt.datetime = datafield(default=DatetimeUtil.from_fields(2003, 5, 1, 10, 15, 0))
    """Stub field."""

    key_uuid_field: UUID = datafield(default=UUID("1A" * 16))
    """Stub field."""

    key_bytes_field: bytes = datafield(default=bytes([100, 110, 120]))
    """Stub field."""

    key_enum_field: StubIntEnum = datafield(default=StubIntEnum.ENUM_VALUE_2)
    """Stub field."""

    obj_str_field: str = datafield(default="abc")
    """Stub field."""

    obj_float_field: float = datafield(default=1.23)
    """Stub field."""

    obj_bool_field: bool = datafield(default=True)
    """Stub field."""

    obj_int_field: int = datafield(default=123)
    """Stub field."""

    obj_long_field: int = datafield(default=9007199254740991, subtype="long")
    """The default is maximum safe signed int for JSON: 2^53 - 1."""

    obj_date_field: dt.date = datafield(default=DateUtil.from_fields(2003, 5, 1))
    """Stub field."""

    obj_time_field: dt.time = datafield(default=TimeUtil.from_fields(10, 15, 30))
    """Stub field."""

    obj_date_time_field: dt.datetime = datafield(default=DatetimeUtil.from_fields(2003, 5, 1, 10, 15, 0))
    """Stub field."""

    obj_uuid_field: UUID = datafield(default=UUID("1A" * 16))
    """Stub field."""

    obj_bytes_field: bytes = datafield(default=bytes([100, 110, 120]))
    """Stub field."""

    obj_enum_field: StubIntEnum = datafield(default=StubIntEnum.ENUM_VALUE_1)
    """Stub field."""

    def get_key(self) -> StubDataclassPrimitiveFieldsKey:
        return (
            type(self),
            self.key_str_field,
            self.key_float_field,
            self.key_bool_field,
            self.key_int_field,
            self.key_long_field,
            self.key_date_field,
            self.key_time_field,
            self.key_date_time_field,
            self.key_uuid_field,
            self.key_bytes_field,
            self.key_enum_field,
        )
