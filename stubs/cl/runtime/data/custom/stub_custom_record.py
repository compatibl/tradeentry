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
from typing import Any, Dict, Optional
from cl.runtime.storage.context import Context
from cl.runtime.data.record import Record
from stubs.cl.runtime.data.custom.stub_custom_record_key import StubCustomRecordKey


class StubCustomRecord(StubCustomRecordKey, Record):
    """Stub record used in tests."""

    float_field: Optional[float]
    """Float attribute of base class."""

    def __init__(self, *,
                 str_field: str = 'abc',
                 int_field: int = 123,
                 float_field: float = 4.56):
        """Initialize instance attributes."""

        super().__init__(
            str_field=str_field,
            int_field=int_field
        )

        self.float_field = float_field

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary containing other dictionaries, lists and primitive types."""
        return super().to_dict() | {
            'float_field': self.float_field,
        }
