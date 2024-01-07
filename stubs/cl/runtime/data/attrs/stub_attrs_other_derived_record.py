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
from typing import Optional
from cl.runtime.data.index_util import index_fields
from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_base_record import StubAttrsBaseRecord


@index_fields('other_float_field_2, other_string_field_2, -record_index')
@attrs_record
class StubAttrsOtherDerivedRecord(StubAttrsBaseRecord):
    """Another type derived from StubAttrsBaseRecord."""

    other_float_field_2: Optional[float] = attrs_field()
    """Stub field."""

    other_string_field_2: Optional[str] = attrs_field()
    """Stub field."""

    @staticmethod
    def create(*, record_id: str = "abc", record_index: int = 123, version: int = 0) -> StubAttrsOtherDerivedRecord:
        """Create with stub data."""

        obj = StubAttrsOtherDerivedRecord()
        obj.record_id = record_id
        obj.record_index = record_index
        obj.version = version

        obj.float_field = 300.0
        obj.date_field = DateUtil.from_fields(2003, 5, 1)
        obj.time_field = DateTimeUtil.from_fields(10, 15, 30)  # 10:15:30
        obj.date_time_field = DateUtil.from_fields(2003, 5, 1, 10, 15)  # 2003-05-01T10:15:00
        obj.other_string_field_2 = 'abc'
        obj.other_float_field_2 = 200.0

        return obj
