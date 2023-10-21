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

from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

import cl.runtime as rt
from cl.runtime.core.storage.class_record import ClassRecord

if TYPE_CHECKING:
    from cl.runtime.stubs.storage.stub_cyclic_b import StubCyclicB


@dataclass
class StubCyclicA(ClassRecord):
    """Stub class A with a field whose type is key for class B."""

    a_id: str = rt.class_field()
    """Unique identifier."""

    b: Union[str, StubCyclicB] = rt.class_field()
    """Key for class B."""

    @staticmethod
    def get_common_base():
        """Type of the common base for all classes stored in the same table as this class."""
        return StubCyclicA

    @staticmethod
    def create_key(a_id: str) -> str:
        """Create primary key from arguments in semicolon-delimited string format."""
        return a_id

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return self.a_id

    @staticmethod
    def create_sample_key() -> str:
        """Return PK populated with sample data."""
        return StubCyclicA.create_key('abc')

    @staticmethod
    def create_sample_record(context: rt.Context) -> StubCyclicA:
        """Return an instance of this class populated with sample data."""

        # Import inside function to avoid cyclic reference error
        from cl.runtime.stubs.storage.stub_cyclic_b import StubCyclicB

        obj = StubCyclicA()
        obj.context = context
        obj.a_id = "abc"
        obj.b = StubCyclicB.create_key("abc")
        obj.init()
        return obj
