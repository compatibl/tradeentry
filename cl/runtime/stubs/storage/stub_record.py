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

import cl.runtime as rt


class StubRecord(rt.Record):
    """Stub record used in tests."""

    key_field_str: Optional[str]
    """First primary key attribute."""

    key_field_int: Optional[int]
    """Second primary key attribute."""

    base_field_str: Optional[str]
    """String attribute of base class."""

    base_field_float: Optional[float]
    """Float attribute of base class."""

    def __init__(self):
        """Initialize instance attributes."""
        super().__init__()
        self.key_field_str = None
        self.key_field_int = None
        self.base_field_str = None
        self.base_field_float = None

    @staticmethod
    def get_common_base():
        """Type of the common base for all classes stored in the same table as this class."""
        return StubRecord

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return f"{self.key_field_str};{self.key_field_int}"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize self as dictionary (may return shallow copy)."""
        return {
            'key_field_str': self.key_field_str,
            'key_field_int': self.key_field_int,
            'base_field_str': self.base_field_str,
            'base_field_float': self.base_field_float,
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Populate self from dictionary (must perform deep copy)."""
        self.key_field_str = data.get('key_field_str')
        self.key_field_int = data.get('key_field_int')
        self.base_field_str = data.get('base_field_str')
        self.base_field_float = data.get('base_field_float')
        # TODO: detect extra fields in dict which are not in class and raise error

    @staticmethod
    def create_sample_record(context: rt.Context) -> StubRecord:
        """Return an instance of this class populated with sample data."""

        obj = StubRecord()
        obj.context = context
        obj.key_field_str = 'abc'
        obj.key_field_int = 123
        obj.base_field_str = 'def'
        obj.base_field_float = 4.56
        obj.update()
        return obj
