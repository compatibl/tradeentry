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
from cl.runtime.classes.dataclasses.dataclass_mixin import datafield
from typing import TYPE_CHECKING
from cl.runtime.classes.dataclasses.dataclass_mixin import DataclassMixin
from typing import Tuple, Type

if TYPE_CHECKING:
    from stubs.cl.runtime.classes.dataclasses.stub_dataclass_cyclic_b import StubDataclassCyclicB, StubDataclassCyclicBKey

StubDataclassCyclicAKey = Tuple[Type['StubDataclassCyclicA'], 'StubDataclassCyclicBKey']


@dataclass
class StubDataclassCyclicA(DataclassMixin):
    """Stub class A with a field whose type is key for class B."""

    key: StubDataclassCyclicBKey | None = datafield()
    """Key for class B."""

    b: StubDataclassCyclicB | None = datafield()
    """Key for class B."""

    def get_key(self) -> StubDataclassCyclicAKey:
        return StubDataclassCyclicA, self.key

    @staticmethod
    def create() -> StubDataclassCyclicA:
        """Create an instance of this class populated with sample data."""

        # Import inside function to avoid cyclic reference error
        from stubs.cl.runtime.classes.dataclasses.stub_dataclass_cyclic_b import StubDataclassCyclicB

        obj = StubDataclassCyclicA()
        obj.key = StubDataclassCyclicB(id="b").get_key()
        obj.b = StubDataclassCyclicB()
        return obj
