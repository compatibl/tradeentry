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
from typing import TYPE_CHECKING, Union
from cl.runtime.storage.record import Record
if TYPE_CHECKING:
    from cl.runtime.storage.stubs.stub_cyclic_a import StubCyclicA


@data_class
class StubCyclicB(Record):
    """Stub class A with a field whose type is key for class B."""

    b_id: str = data_field()
    """Unique identifier."""

    a: Union[str, StubCyclicA] = data_field()
    """Key for class A."""

    @staticmethod
    def create_key(b_id: str) -> str:
        """Create primary key from arguments in semicolon-delimited string format."""
        return b_id

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return self.b_id

    @staticmethod
    def create_sample_key() -> str:
        """Return PK populated with sample data."""
        return StubCyclicB.create_key('abc')

    @staticmethod
    def create_sample_record(context: Context) -> StubCyclicB:
        """Return an instance of this class populated with sample data."""

        # Import inside function to avoid cyclic reference error
        from cl.runtime.storage.stubs.stub_cyclic_a import StubCyclicA

        obj = StubCyclicB()
        obj.context = context
        obj.b_id = "abc"
        obj.a = StubCyclicA.create_key("abc")
        obj.init()
        return obj
