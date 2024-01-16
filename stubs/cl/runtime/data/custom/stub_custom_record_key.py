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
from typing_extensions import Self
from typing import Any, Dict, Optional
from cl.runtime.data.context import Context
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.data.key import Key


class StubCustomRecordKey(Key):
    """Stub record used in tests."""

    key_field_str: Optional[str]
    """First primary key attribute."""

    key_field_int: Optional[int]
    """Second primary key attribute."""

    def __init__(self, *,
                 key_field_str: str = 'abc',
                 key_field_int: int = 123
                 ):
        """Initialize instance attributes."""
        self.key_field_str = key_field_str
        self.key_field_int = key_field_int

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary containing other dictionaries, lists and primitive types."""
        return {
            'key_field_str': self.key_field_str,
            'key_field_int': self.key_field_int
        }

    def get_table(self) -> str:
        """Name of the database table where the record for this key is stored."""
        return f"{type(self).__module__}.{type(self).__name__}"

    def get_key(self) -> str:
        """Key as string in semicolon-delimited string format without table name."""
        return f"{self.key_field_str};{self.key_field_int}"


