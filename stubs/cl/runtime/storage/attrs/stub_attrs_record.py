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
from cl.runtime.storage.handler_util import handler
from cl.runtime.storage.viewer_util import viewer
from cl.runtime.storage.index_util import index_fields
from cl.runtime.storage.context import Context
from cl.runtime.storage.data import Data
from cl.runtime.storage.record import Record
from cl.runtime.storage.attrs_record_util import attrs_record
from cl.runtime.storage.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_data import StubAttrsData
from stubs.cl.runtime.data.attrs.stub_attrs_record_key import StubAttrsRecordKey
from stubs.cl.runtime.data.enum.stub_int_enum import StubIntEnum

_logger = Logger(__name__)


def data_list_field_factory():
    """Create an instance of List[StubAttrsData] with stub data."""
    return [
        StubAttrsData(str_field="abc", int_field=1),
        StubAttrsData(str_field="xyz", int_field=2)
        ]


@index_fields('version')
@index_fields('str_field, int_field, -version', 'CustomIndexName')
@attrs_record
class StubAttrsRecord(StubAttrsRecordKey, Record):
    """Stub record base class."""
    
    version: int = attrs_field(default=0)
    """Stub version field."""

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

    @viewer(label="Relabeled Viewer New Label")
    def relabeled_viewer(self) -> None:
        """Viewer whose label is modified."""
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
        """Stub method."""
        pass

    def handler_with_args(self, arg_1: str, arg_2: str) -> str:
        """Stub method."""
        return arg_1 + arg_2

    def handler_with_args_and_optional(self, arg_1: str, arg_2: str, arg_3: str = None) -> str:
        """Stub method."""
        return arg_1 + arg_2

    def handler_with_reserved_param_name(self, from_: dt.date = None) -> dt.date:
        """Stub method."""
        return from_

    def handler_with_error(self):
        """Stub method."""
        raise RuntimeError("Error in handler.")
