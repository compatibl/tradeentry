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
from uuid import UUID

from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.storage.record import Record
from cl.runtime.storage.attrs import attrs_field, attrs_class
from cl.runtime.primitive.time_util import TimeUtil
from stubs.cl.runtime.storage.enum.stub_int_enum import StubIntEnum
from stubs.cl.runtime.storage.attrs.stub_attrs_primitive_fields_key import StubAttrsPrimitiveFieldsKey


@attrs_class
class StubAttrsPrimitiveFields(StubAttrsPrimitiveFieldsKey, Record):
    """Stub record whose elements are primitive types."""

    base_str_field: str = attrs_field(default="abc")
    """Stub field."""

    base_float_field: float = attrs_field(default=1.23)
    """Stub field."""

    base_bool_field: bool = attrs_field(default=True)
    """Stub field."""

    base_int_field: int = attrs_field(default=123)
    """Stub field."""

    base_long_field: int = attrs_field(default=9007199254740991, subtype='long')
    """The default is maximum safe signed int for JSON: 2^53 - 1."""

    base_date_field: dt.date = attrs_field(default=DateUtil.from_fields(2003, 5, 1))
    """Stub field."""

    base_time_field: dt.time = attrs_field(default=TimeUtil.from_fields(10, 15, 30))
    """Stub field."""

    base_date_time_field: dt.datetime = attrs_field(default=DateTimeUtil.from_fields(2003, 5, 1, 10, 15))
    """Stub field."""

    base_uuid_field: UUID = attrs_field(default=UUID('1A' * 16))
    """Stub field."""

    base_bytes_field: bytes = attrs_field(default=bytes([100, 110, 120]))
    """Stub field."""

    base_enum_field: StubIntEnum = attrs_field(default=StubIntEnum.ENUM_VALUE_1)
    """Stub field."""

    base_str_key_field: str = attrs_field(default="StubAttrsRecord;abc;123", subtype='StubRecordKey')
    """Stub field."""

    base_generic_key_field: str = attrs_field(default="StubAttrsRecord;abc;123", subtype='GenericKey')
    """Stub field."""
