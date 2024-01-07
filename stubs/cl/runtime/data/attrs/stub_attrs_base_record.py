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
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.data.attrs.stubs.stub_attrs_base_data import StubAttrsBaseData
from cl.runtime.data.attrs.stubs.stub_attrs_base_record_key import StubAttrsBaseRecordKey
from cl.runtime.data.attrs.stubs.stub_attrs_enum import StubAttrsEnum

_logger = Logger(__name__)


@index_fields('float_field, date_field, enum_value')
@index_fields('date_field')
@index_fields('record_id, -version', 'CustomIndexName')
@index_fields('-record_index')
@index_fields('nested_data_list.data.float_field_3')
@index_fields('nested_attrs_field.data.float_field_3')
@attrs_record
class StubAttrsBaseRecord(StubAttrsBaseRecordKey):
    """Stub record base class."""

    float_field: Optional[float] = attrs_field()
    """Stub field."""

    date_field: Optional[dt.date] = attrs_field()
    """Stub field."""

    enum_value: Optional[StubAttrsEnum] = attrs_field()
    """Stub field."""

    version: Optional[int] = attrs_field()
    """Stub field."""

    time_field: Optional[dt.time] = attrs_field()
    """Stub field."""

    date_time_field: Optional[dt.datetime] = attrs_field()
    """Stub field."""

    long_field: Optional[int] = attrs_field(subtype='long')
    """Stub field."""

    bytes_field: Optional[bytes] = attrs_field()
    """Stub field."""

    nested_attrs_field: Optional[StubAttrsBaseData] = attrs_field()
    """Stub field."""

    nested_data_list: Optional[List[StubAttrsBaseData]] = attrs_field()
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
        enum_arg: StubAttrsEnum,
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

    @staticmethod
    def create(*, record_id: str = "abc", record_index: int = 123, version: int = 0) -> StubAttrsBaseRecord:
        """Create with stub data."""

        obj = StubAttrsBaseRecord()
        obj.record_id = record_id
        obj.record_index = record_index
        obj.version = version

        obj.float_field = 123.456
        obj.enum_value = StubAttrsEnum.ENUM_VALUE_2
        obj.version = 1
        obj.date_field = DateUtil.from_str("2023-05-01")
        obj.time_field = TimeUtil.from_str("10:15:00")
        obj.date_time_field = DateTimeUtil.from_str("2023-05-01T10:15:00")
        obj.long_field = 100 * 2147483647
        obj.bytes_field = bytes([100, 110, 120])
        obj.nested_attrs_field = StubAttrsBaseData(string_field="abc", float_field=1.0)
        obj.nested_data_list = [
            StubAttrsBaseData(string_field="abc", float_field=1.0),
            StubAttrsBaseData(string_field="xyz", float_field=2.0)
        ]

        return obj
