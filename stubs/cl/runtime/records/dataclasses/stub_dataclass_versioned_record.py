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

from cl.runtime.records.dataclasses.dataclass_mixin import DataclassMixin
from dataclasses import dataclass
from stubs.cl.runtime.records.dataclasses.stub_dataclass_versioned_record_key import StubDataclassVersionedRecordKey


@dataclass(slots=True)
class StubDataclassVersionedRecord(DataclassMixin):
    """Stub record base class."""

    id: str = "abc"
    """Stub field."""

    version: int = 0
    """Stub version field."""

    def get_key(self) -> StubDataclassVersionedRecordKey:
        return type(self), self.id
