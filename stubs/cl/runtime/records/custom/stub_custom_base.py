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

from typing import Dict
from typing import Type
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.db.data_source_types import TDataDict
from cl.runtime.db.data_source_types import TDataField
from stubs.cl.runtime.records.custom.stub_custom_base_key import StubCustomBaseKey


class StubCustomBase(StubCustomBaseKey, RecordMixin[StubCustomBaseKey]):
    """Stub record used in tests."""

    float_field: float | None
    """Float attribute of base class."""

    def __init__(self, *, str_field: str = "abc", int_field: int = 123, float_field: float = 4.56):
        """Initialize instance attributes."""

        RecordMixin.__init__(self)
        StubCustomBaseKey.__init__(self, str_field=str_field, int_field=int_field)

        self.float_field = float_field

    def to_dict(self) -> Dict[str, TDataField]:
        return {
            "str_field": self.str_field,
            "int_field": self.int_field,
            "float_field": self.float_field,
        }

    def get_key(self) -> StubCustomBaseKey:
        return StubCustomBaseKey(str_field=self.str_field, int_field=self.int_field)
