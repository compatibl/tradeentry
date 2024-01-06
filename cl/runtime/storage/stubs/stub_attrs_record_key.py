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
from cl.runtime.decorators.attrs_key_decorator import attrs_key
from cl.runtime.decorators.data_field_decorator import data_field
from cl.runtime.storage.key import Key


@attrs_key
class StubAttrsRecordKey(Key):
    """Stub dataclass-based record sample used in tests."""

    key_field_str: str = data_field()
    """First primary key attribute."""

    key_field_int: int = data_field()
    """Second primary key attribute."""

    @staticmethod
    def create_key(key_field_str: str = "abc", key_field_int: int = 0) -> StubAttrsRecordKey:
        """Create from fields with default values."""
        return StubAttrsRecordKey(key_field_str=key_field_str, key_field_int=key_field_int)
