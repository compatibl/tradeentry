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
import datetime as dt
from logging import Logger
from typing import List, Optional
from cl.runtime.data.handler_util import handler
from cl.runtime.data.viewer_util import viewer
from cl.runtime.data.index_util import index_fields
from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.primitive.time_util import TimeUtil
from cl.runtime.data.context import Context
from cl.runtime.data.data import Data
from cl.runtime.data.record import Record
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_data import StubAttrsData
from stubs.cl.runtime.data.attrs.stub_attrs_record_key import StubAttrsRecordKey
from stubs.cl.runtime.data.enum.stub_int_enum import StubIntEnum

_logger = Logger(__name__)

def nested_data_list_factory():
    """Create an instance of List[StubAttrsData] with stub data."""
    return [
        StubAttrsData(string_field="abc", float_field=1.0),
        StubAttrsData(string_field="xyz", float_field=2.0)
        ]


@index_fields('float_field, date_field, enum_value')
@index_fields('date_field')
@index_fields('record_id, -version', 'CustomIndexName')
@index_fields('-record_index')
@index_fields('nested_data_list.data.float_field_3')
@index_fields('nested_attrs_field.data.float_field_3')
@attrs_record
class StubAttrsRecord(StubAttrsRecordKey, Record):
    """Stub record base class."""
    
    version: Optional[int] = attrs_field(default=0)
    """Stub field."""

    float_field: Optional[float] = attrs_field(default=123.456)
    """Stub field."""

    date_field: Optional[dt.date] = attrs_field(default=DateUtil.from_str("2023-05-01"))
    """Stub field."""

    enum_value: Optional[StubIntEnum] = attrs_field(default=StubIntEnum.ENUM_VALUE_2)
    """Stub field."""

    time_field: Optional[dt.time] = attrs_field(default=TimeUtil.from_str("10:15:00"))
    """Stub field."""

    date_time_field: Optional[dt.datetime] = attrs_field(default=DateTimeUtil.from_str("2023-05-01T10:15:00"))
    """Stub field."""

    long_field: Optional[int] = attrs_field(default=9007199254740991, subtype='long')
    """The default is maximum safe signed int for JSON: 2^53 - 1."""

    bytes_field: Optional[bytes] = attrs_field(default=bytes([100, 110, 120]))
    """Stub field."""

    nested_attrs_field: Optional[StubAttrsData] = attrs_field(factory=StubAttrsData)
    """Stub field."""

    nested_data_list: Optional[List[StubAttrsData]] = attrs_field(factory=nested_data_list_factory)
    """Stub field."""

    @handler()
    def non_virtual_base_handler(self) -> None:
        """Stub handler."""
        pass

    @handler()
    def virtual_base_handler(self) -> None:
        """Stub handler."""
        pass

    @viewer()
    def default_named_viewer(self) -> None:
        """Stub viewer."""
        pass

    @viewer(label="After Rename")
    def before_rename(self) -> None:
        """Stub viewer."""
        pass

    def handler_with_arguments(
        self,
        int_arg: int,
        datetime_arg: dt.datetime,
        enum_arg: StubIntEnum,
        data_arg: Data,
    ) -> None:
        _logger.info(f"handler_with_arguments(int_arg={int_arg} datetime_arg={datetime_arg}"
                     f"enum_arg={enum_arg} data_arg={data_arg})")

    @staticmethod
    def static_method(context: Context):
        """Sample static method."""
        pass

    @classmethod
    def class_method(cls, context: Context):
        """Sample class method."""
        pass

    def handler_with_args(self, arg_1: str, arg_2: str) -> str:
        return arg_1 + arg_2

    def handler_with_args_and_optional(self, arg_1: str, arg_2: str, arg_3: str = None) -> str:
        return arg_1 + arg_2

    def handler_with_reserved_param_name(self, from_: dt.date = None) -> dt.date:
        """
        Parameters
        ----------
        from_ : date, name=From
        """
        return from_

    def handler_with_error(self):
        raise Exception("Error in handler")
