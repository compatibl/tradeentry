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
from cl.runtime.decorators.attrs_record_decorator import attrs_record
from cl.runtime.decorators.data_field_decorator import data_field
from cl.runtime import Context
from cl.runtime.storage.stubs.stub_attrs_record import StubAttrsRecord


@attrs_record
class StubDerivedAttrsRecord(StubAttrsRecord):
    """Stub derived dataclass-based record sample used in tests."""

    derived_field_str: str = data_field()
    """String attribute of base class."""

    derived_field_float: float = data_field()
    """Float attribute of base class."""

    @staticmethod
    def create(context: Context) -> StubDerivedAttrsRecord:
        """Return an instance of this class populated with sample data."""

        obj = StubDerivedAttrsRecord()
        obj.context = context
        obj.key_field_str = 'abc'
        obj.key_field_int = 123
        obj.base_field_str = 'def'
        obj.base_field_float = 4.56
        obj.derived_field_str = 'def'
        obj.derived_field_float = 4.56
        obj.init()
        return obj
