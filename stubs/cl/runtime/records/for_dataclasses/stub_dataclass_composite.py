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
from cl.runtime.records.record_mixin import RecordMixin
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_composite_key import StubDataclassCompositeKey


@dataclass(slots=True, kw_only=True)
class StubDataclassComposite(StubDataclassCompositeKey, RecordMixin[StubDataclassCompositeKey]):
    """Stub for a composite key that contains other key fields."""

    def get_key(self) -> StubDataclassCompositeKey:
        return StubDataclassCompositeKey(
            primitive=self.primitive,
            embedded_1=self.embedded_1,
            embedded_2=self.embedded_2,
        )
