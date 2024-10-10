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
from typing import List
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_data import StubDataclassData
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_optional_fields_key import StubDataclassOptionalFieldsKey
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_record import StubDataclassRecord
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_record import StubDataclassRecordKey


@dataclass(slots=True, kw_only=True)
class StubDataclassOptionalFields(StubDataclassOptionalFieldsKey, RecordMixin[StubDataclassOptionalFieldsKey]):
    """Stub derived class."""

    optional_str: str | None = "xyz"
    """Optional string."""

    required_list_of_optional_str: List[str | None] = field(default_factory=lambda: ["abc", None])
    """Required list of optional strings."""

    optional_list_of_optional_str: List[str | None] | None = None
    """Optional list of optional strings."""

    optional_float: float | None = 1.23
    """Optional float."""

    required_list_of_optional_float: List[float | None] = field(default_factory=lambda: [1.23, None])
    """Required list of optional floats."""

    optional_list_of_optional_float: List[float | None] | None = None
    """Optional list of optional floats."""

    # TODO: Add a complete set of optional primitive field types and lists

    optional_data: StubDataclassData | None = None
    """Optional data."""

    required_list_of_optional_data: List[StubDataclassData | None] = field(default_factory=lambda: [StubDataclassData(), None])
    """Required list of optional data."""

    optional_list_of_optional_data: List[StubDataclassData | None] | None = None
    """Optional list of optional data."""

    optional_key: StubDataclassRecordKey | None = None
    """Optional key."""

    required_list_of_optional_key: List[StubDataclassRecordKey | None] = field(default_factory=lambda: [StubDataclassRecordKey(), None])
    """Required list of optional key."""

    optional_list_of_optional_key: List[StubDataclassRecordKey | None] | None = None
    """Optional list of optional key."""

    optional_record: StubDataclassRecord | None = None
    """Optional record."""

    required_list_of_optional_record: List[StubDataclassRecord | None] = field(default_factory=lambda: [StubDataclassRecord(), None])
    """Required list of optional record."""

    optional_list_of_optional_record: List[StubDataclassRecord | None] | None = None
    """Optional list of optional record."""

    def get_key(self) -> StubDataclassOptionalFieldsKey:
        return StubDataclassOptionalFieldsKey(id=self.id)
