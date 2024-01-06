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
from cl.runtime.storage.context import Context
from cl.runtime.decorators.data_field_decorator import data_field
from cl.runtime.storage.record import Record
from cl.runtime.decorators.attrs_record_decorator import attrs_record
from cl.runtime.storage.stubs.stub_attrs_record_key import StubAttrsRecordKey


@attrs_record
class StubAttrsRecord(StubAttrsRecordKey, Record):
    """Stub record used in tests."""

    base_field_str: Optional[str] = data_field()
    """String attribute of base class."""

    base_field_float: Optional[float] = data_field()
    """Float attribute of base class."""

    @staticmethod
    def create(
            context: Context = None,
            *,
            key_field_str: str = "abc",
            key_field_int: int = 0,
            base_field_str: str = "xyz",
            base_field_float: float = 1.0
    ) -> StubAttrsRecord:
        """Create from fields with default values."""

        obj = StubAttrsRecord()
        obj.context = context
        obj.key_field_str = key_field_str
        obj.key_field_int = key_field_int
        obj.base_field_str = base_field_str
        obj.base_field_float = base_field_float
        obj.init()
        return obj
