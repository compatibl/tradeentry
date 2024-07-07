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
from cl.runtime.records.dataclasses_util import datafield
from cl.runtime.records.key_mixin import KeyMixin
from dataclasses import dataclass
from stubs.cl.runtime.records.enum.stub_int_enum import StubIntEnum
from typing import Type
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class StubDataclassPrimitiveFieldsKey(KeyMixin):
    """Stub record whose elements are primitive types."""

    key_str_field: str = "abc"
    """Stub field."""

    key_float_field: float = 1.23
    """Stub field."""

    key_bool_field: bool = True
    """Stub field."""

    key_int_field: int = 123
    """Stub field."""

    key_long_field: int = datafield(default=9007199254740991, subtype="long")  # TODO: Rename subtype?
    """The default is maximum safe signed int for JSON: 2^53 - 1."""
    # TODO: Define maximum safe long in Util class

    key_date_field: dt.date = DateUtil.from_fields(2003, 5, 1)
    """Stub field."""

    key_time_field: dt.time = TimeUtil.from_fields(10, 15, 30)
    """Stub field."""

    key_date_time_field: dt.datetime = DatetimeUtil.from_fields(2003, 5, 1, 10, 15, 0)
    """Stub field."""

    key_uuid_field: UUID = UUID("1A" * 16)
    """Stub field."""

    key_bytes_field: bytes = bytes([100, 110, 120])
    """Stub field."""

    key_enum_field: StubIntEnum = StubIntEnum.ENUM_VALUE_2
    """Stub field."""

    def get_key_type(self) -> Type:
        return StubDataclassPrimitiveFieldsKey
