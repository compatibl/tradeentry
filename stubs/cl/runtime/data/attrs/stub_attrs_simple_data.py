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
from cl.runtime.data.attrs.attrs_data_util import attrs_data
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.data.data import Data


@attrs_data
class StubAttrsSimpleData(Data):
    """Dataclass-based serializable data sample used in tests."""

    base_field_str: str = attrs_field()
    """String attribute of base class."""

    base_field_int: int = attrs_field()
    """Float attribute of base class."""

    @staticmethod
    def create(
            *,
            base_field_str: str = 'abc',
            base_field_int: int = 123
    ) -> StubAttrsSimpleData:
        """Create an instance of this class populated with sample data."""
        obj = StubAttrsSimpleData()
        obj.base_field_str = base_field_str
        obj.base_field_int = base_field_int
        return obj
