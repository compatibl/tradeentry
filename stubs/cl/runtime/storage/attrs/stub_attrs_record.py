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
from cl.runtime.decorators.handler_decorator import handler
from cl.runtime.decorators.viewer_decorator import viewer
from cl.runtime.storage.attrs import data_class
from cl.runtime.storage.attrs import data_field
from cl.runtime.storage.data_mixin import DataMixin
from cl.runtime.storage.index_util import index_fields
from cl.runtime.storage.record_mixin import RecordMixin
from logging import Logger
from stubs.cl.runtime.storage.attrs.stub_attrs_data import StubAttrsData
from stubs.cl.runtime.storage.attrs.stub_attrs_record_key import StubAttrsRecordKey
from stubs.cl.runtime.storage.enum.stub_int_enum import StubIntEnum

_logger = Logger(__name__)


def data_list_field_factory():
    """Create an instance of List[StubAttrsData] with stub data."""
    return [StubAttrsData(str_field="abc", int_field=1), StubAttrsData(str_field="xyz", int_field=2)]


@index_fields("version")
@index_fields("str_field, int_field, -version", "CustomIndexName")
@data_class
class StubAttrsRecord(StubAttrsRecordKey, RecordMixin):
    """Stub record base class."""

    version: int = data_field(default=0)
    """Stub version field."""
