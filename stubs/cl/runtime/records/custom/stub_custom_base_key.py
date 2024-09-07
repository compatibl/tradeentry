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

from cl.runtime.records.key_mixin import KeyMixin
from cl.runtime.storage.data_source_types import TDataField
from typing import Dict
from typing import Type


class StubCustomBaseKey(KeyMixin):
    """Stub record used in tests."""

    str_field: str | None
    """First primary key attribute."""

    int_field: int | None
    """Second primary key attribute."""

    def __init__(self, str_field: str = "abc", int_field: int = 123):
        """Initialize instance attributes."""

        self.str_field = str_field
        self.int_field = int_field

    def to_dict(self) -> Dict[str, TDataField]:
        return {
            "str_field": self.str_field,
            "int_field": self.int_field,
        }

    @classmethod
    def get_key_type(cls) -> Type:
        return StubCustomBaseKey
