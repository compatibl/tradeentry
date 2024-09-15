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
from dataclasses import dataclass
from uuid import UUID
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.primitive.time_util import TimeUtil
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from stubs.cl.runtime.records.enum.stub_int_enum import StubIntEnum
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_primitive_fields_key import StubDataclassPrimitiveFieldsKey


@dataclass(slots=True, kw_only=True)
class StubDataclassPrimitiveFields(StubDataclassPrimitiveFieldsKey, RecordMixin[StubDataclassPrimitiveFieldsKey]):
    """Stub record whose elements are primitive types."""

    obj_str_field: str = "abc"
    """Stub field."""

    obj_float_field: float = 1.23
    """Stub field."""

    obj_bool_field: bool = True
    """Stub field."""

    obj_int_field: int = 123
    """Stub field."""

    obj_long_field: int = field(default=9007199254740991, subtype="long")
    """The default is maximum safe signed int for JSON: 2^53 - 1."""

    obj_date_field: dt.date = DateUtil.from_fields(2003, 5, 1)
    """Stub field."""

    obj_time_field: dt.time = TimeUtil.from_fields(10, 15, 30)
    """Stub field."""

    obj_date_time_field: dt.datetime = DatetimeUtil.from_fields(2003, 5, 1, 10, 15, 0)
    """Stub field."""

    obj_uuid_field: UUID = UUID("1A" * 16)
    """Stub field."""

    obj_bytes_field: bytes = bytes([100, 110, 120])
    """Stub field."""

    obj_enum_field: StubIntEnum = StubIntEnum.ENUM_VALUE_1
    """Stub field."""

    def get_key(self) -> StubDataclassPrimitiveFieldsKey:
        return StubDataclassPrimitiveFieldsKey(
            key_str_field=self.key_str_field,
            key_float_field=self.key_float_field,
            key_bool_field=self.key_bool_field,
            key_int_field=self.key_int_field,
            key_long_field=self.key_long_field,
            key_date_field=self.key_date_field,
            key_time_field=self.key_time_field,
            key_date_time_field=self.key_date_time_field,
            key_uuid_field=self.key_uuid_field,
            key_bytes_field=self.key_bytes_field,
            key_enum_field=self.key_enum_field,
        )
