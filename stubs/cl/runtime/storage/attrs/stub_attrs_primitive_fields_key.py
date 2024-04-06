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
from cl.runtime.storage.attrs import data_class
from cl.runtime.storage.attrs import data_field
from cl.runtime.storage.key_mixin import KeyMixin
from stubs.cl.runtime.storage.enum.stub_int_enum import StubIntEnum
from uuid import UUID


@data_class
class StubAttrsPrimitiveFieldsKey(KeyMixin):
    str_field: str = data_field(default="abc")
    """Stub field."""

    float_field: float = data_field(default="1.23")
    """Stub field."""

    bool_field: bool = data_field(default=True)
    """Stub field."""

    int_field: int = data_field(default=123)
    """Stub field."""

    long_field: int = data_field(default=9007199254740991, subtype="long")  # Rename subtype
    """The default is maximum safe signed int for JSON: 2^53 - 1."""
    # TODO: Define maximum safe long in Util class

    date_field: dt.date = data_field(default=DateUtil.from_fields(2003, 5, 1))
    """Stub field."""

    time_field: dt.time = data_field(default=TimeUtil.from_fields(10, 15, 30))
    """Stub field."""

    date_time_field: dt.datetime = data_field(default=DateTimeUtil.from_fields(2003, 5, 1, 10, 15))
    """Stub field."""

    uuid_field: UUID = data_field(default=UUID("1A" * 16))
    """Stub field."""

    bytes_field: bytes = data_field(default=bytes([100, 110, 120]))
    """Stub field."""

    enum_field: StubIntEnum = data_field(default=StubIntEnum.ENUM_VALUE_2)
    """Stub field."""

    str_key_field: str = data_field(default="abc;123", subtype="StubRecordKey")  # Rename subtype
    """Stub field."""

    generic_key_field: str = data_field(default="StubAttrsRecord;abc;123", subtype="GenericKey")  # Rename subtype
    """Stub field."""
