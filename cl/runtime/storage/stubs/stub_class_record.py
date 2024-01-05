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
from cl.runtime.decorators.data_class_decorator import data_class
from cl.runtime.decorators.data_field_decorator import data_field
from cl.runtime.storage.record import Record


@data_class
class StubClassRecord(Record):
    """Stub dataclass-based record sample used in tests."""

    key_field_str: str = data_field()
    """First primary key attribute."""

    key_field_int: int = data_field()
    """Second primary key attribute."""

    base_field_str: str = data_field()
    """String attribute of base class."""

    base_field_float: float = data_field()
    """Float attribute of base class."""

    base_field_long: int = data_field(subtype='long', label="Custom Label", optional=True)
    """Optional long attribute of base class with custom label."""

    @staticmethod
    def get_common_base():
        """Type of the common base for all classes stored in the same table as this class."""
        return StubClassRecord

    @staticmethod
    def create_key(key_field_str: str, key_field_int: int) -> str:
        """Create primary key from arguments in semicolon-delimited string format."""
        return f'{key_field_str};{key_field_int}'

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return f'{self.key_field_str};{self.key_field_int}'

    @staticmethod
    def create_sample_key() -> str:
        """Return PK populated with sample data."""
        return StubClassRecord.create_key('abc', 123)

    @staticmethod
    def create_sample_record(context: Context) -> StubClassRecord:
        """Return an instance of this class populated with sample data."""

        obj = StubClassRecord()
        obj.context = context
        obj.key_field_str = 'abc'
        obj.key_field_int = 123
        obj.base_field_str = 'def'
        obj.base_field_float = 4.56
        obj.init()
        return obj
