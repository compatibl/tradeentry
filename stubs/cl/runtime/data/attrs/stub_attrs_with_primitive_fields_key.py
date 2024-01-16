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

from cl.runtime.data.attrs.attrs_key_util import attrs_key
from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.primitive.ordered_uid import OrderedUid
from cl.runtime.data.record import Record
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.data.key import Key
from cl.runtime.primitive.time_util import TimeUtil
from stubs.cl.runtime.data.attrs.stub_attrs_record_key import StubAttrsRecordKey
from stubs.cl.runtime.data.enum.stub_int_enum import StubIntEnum


@attrs_key
class StubAttrsWithPrimitiveFieldsKey(Key):

    key_int_field: int = attrs_field(default=123)
    """Stub field."""

    key_long_field: int = attrs_field(default=9007199254740991, subtype='long')
    """The default is maximum safe signed int for JSON: 2^53 - 1."""

    key_bool_field: bool = attrs_field(default=True)
    """Stub field."""

    key_string_field: str = attrs_field(default="abc")
    """Stub field."""

    key_enum_field: StubIntEnum = attrs_field(default=StubIntEnum.ENUM_VALUE_2)
    """Stub field."""

    key_date_field: dt.date = attrs_field(default=DateUtil.from_fields(2003, 5, 1))
    """Stub field."""

    key_time_field: dt.time = attrs_field(default=TimeUtil.from_fields(10, 15, 30))
    """Stub field."""

    key_date_time_field: dt.datetime = attrs_field(default=DateTimeUtil.from_fields(2003, 5, 1, 10, 15))
    """Stub field."""

    # TODO: Change type
    key_key_field: Key = attrs_field(factory=StubAttrsRecordKey)
    """Stub field."""

    key_guid_field: OrderedUid = attrs_field(default=OrderedUid('1A' * 16))
    """Stub field."""

