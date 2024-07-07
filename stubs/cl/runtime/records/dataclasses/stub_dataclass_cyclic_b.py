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

from cl.runtime.records.dataclasses_util import datafield
from cl.runtime.records.record_mixin import RecordMixin
from dataclasses import dataclass
from stubs.cl.runtime.records.dataclasses.stub_dataclass_cyclic_b_key import StubDataclassCyclicBKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stubs.cl.runtime.records.dataclasses.stub_dataclass_cyclic_a import StubDataclassCyclicA


@dataclass(slots=True, kw_only=True)
class StubDataclassCyclicB(StubDataclassCyclicBKey, RecordMixin):
    """Stub class A with a field whose type is key for class B."""

    a_obj: StubDataclassCyclicA = datafield()
    """Key for class A."""

    def get_key(self) -> StubDataclassCyclicBKey:
        return StubDataclassCyclicBKey(str_id=self.str_id)

    @staticmethod
    def create() -> StubDataclassCyclicB:
        """Create an instance of this class populated with sample data."""

        # Import inside function to avoid cyclic reference error
        from stubs.cl.runtime.records.dataclasses.stub_dataclass_cyclic_a import StubDataclassCyclicA

        obj = StubDataclassCyclicB()
        obj.str_id = "a"
        obj.a_obj = StubDataclassCyclicA()
        return obj
