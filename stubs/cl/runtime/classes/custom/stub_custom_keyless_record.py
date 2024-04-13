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

from cl.runtime.classes.key_mixin import KeyMixin
from typing import Any
from typing import Dict
from typing import Optional


class StubCustomKeylessRecord(KeyMixin):
    """Stub record used in tests."""

    str_field: Optional[str]
    """First primary key attribute."""

    int_field: Optional[int]
    """Second primary key attribute."""

    float_field: Optional[float]
    """Float attribute of base class."""

    def __init__(self):
        """Initialize instance attributes."""
        self.str_field = "abc"
        self.int_field = 123
        self.float_field = 4.56

    def to_dict(self) -> Dict[str, Any]:
        """Serialize self as dictionary (may return shallow copy)."""
        return {
            "str_field": self.str_field,
            "int_field": self.int_field,
            "float_field": self.float_field,
        }

    def get_table(self) -> str:
        """Name of the database table where the record for this key is stored."""
        return f"{type(self).__module__}.{type(self).__name__}"

    def get_key(self) -> str:
        """Key as string in semicolon-delimited string format without table name."""
        return f"{self.str_field};{self.int_field}"
