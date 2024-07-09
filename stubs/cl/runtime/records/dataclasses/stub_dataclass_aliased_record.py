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

from cl.runtime.records.dataclasses_util import datafield
from cl.runtime.records.record_mixin import RecordMixin
from dataclasses import dataclass
from stubs.cl.runtime.records.dataclasses.stub_dataclass_aliased_record_key import StubDataclassAliasedRecordKey


@dataclass(slots=True, kw_only=True)
class StubDataclassAliasedRecord(
    StubDataclassAliasedRecordKey, RecordMixin[StubDataclassAliasedRecordKey]
):  # TODO: Specify alias
    """Stub record class with typename alias."""

    a: int = datafield()

    def get_key(self) -> StubDataclassAliasedRecordKey:
        return StubDataclassAliasedRecordKey(id=self.id)
