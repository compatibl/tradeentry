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
from cl.runtime.data.context import Context
from cl.runtime.data.record import Record
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.data.attrs.stubs.stub_attrs_simple_record_key import StubAttrsSimpleRecordKey


@attrs_record
class StubAttrsSimpleRecord(StubAttrsSimpleRecordKey, Record):
    """Stub record used in tests."""

    base_field_str: Optional[str] = attrs_field()
    """String attribute of base class."""

    base_field_float: Optional[float] = attrs_field()
    """Float attribute of base class."""

    @staticmethod
    def create(
            context: Context,
            *,
            key_field_str: str = "abc",
            key_field_int: int = 123,
            base_field_str: str = "xyz",
            base_field_float: float = 1.23
    ) -> StubAttrsSimpleRecord:
        """Create an instance of this class populated with sample data."""

        obj = StubAttrsSimpleRecord()
        obj.context = context
        obj.key_field_str = key_field_str
        obj.key_field_int = key_field_int
        obj.base_field_str = base_field_str
        obj.base_field_float = base_field_float
        obj.init()
        return obj
