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

from dataclasses import dataclass
from typing import Type
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_cyclic_b_key import StubDataclassCyclicBKey


@dataclass(slots=True, kw_only=True)
class StubDataclassCyclicAKey(KeyMixin):
    """Stub class A with a field whose type is key for class B."""

    b_key: StubDataclassCyclicBKey = missing()
    """Key for class B."""

    @classmethod
    def get_key_type(cls) -> Type:
        return StubDataclassCyclicAKey
