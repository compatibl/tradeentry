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
from cl.runtime.decorators.attrs_data_decorator import attrs_data
from cl.runtime.decorators.data_field_decorator import data_field
from typing import TYPE_CHECKING, Union
from cl.runtime.storage.record import Record
if TYPE_CHECKING:
    from cl.runtime.storage.stubs.stub_cyclic_b import StubCyclicB


@attrs_data
class StubCyclicA(Record):
    """Stub class A with a field whose type is key for class B."""

    a_id: str = data_field()
    """Unique identifier."""

    b: Union[str, StubCyclicB] = data_field()
    """Key for class B."""

    @staticmethod
    def create() -> StubCyclicA:
        """Return an instance of this class populated with sample data."""

        # Import inside function to avoid cyclic reference error
        from cl.runtime.storage.stubs.stub_cyclic_b import StubCyclicB

        obj = StubCyclicA()
        obj.a_id = "abc"
        obj.b = StubCyclicB()
        obj.b.b_id = "xyz"
        return obj
