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
from typing import TYPE_CHECKING
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_cyclic_a_key import StubDataclassCyclicAKey

if TYPE_CHECKING:
    from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_cyclic_b import StubDataclassCyclicB


@dataclass(slots=True, kw_only=True)
class StubDataclassCyclicA(StubDataclassCyclicAKey, RecordMixin[StubDataclassCyclicAKey]):
    """Stub class A with a field whose type is key for class B."""

    b_obj: StubDataclassCyclicB = missing()
    """Key for class B."""

    def get_key(self) -> StubDataclassCyclicAKey:
        return StubDataclassCyclicAKey(b_key=self.b_key)

    @classmethod
    def create(cls) -> StubDataclassCyclicA:
        """Create an instance of this class populated with sample data."""

        # Import inside function to avoid cyclic reference error
        from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_cyclic_b import StubDataclassCyclicB

        obj = StubDataclassCyclicA()
        obj.b_key = StubDataclassCyclicB(str_id="b").get_key()
        obj.b_obj = StubDataclassCyclicB()
        return obj
