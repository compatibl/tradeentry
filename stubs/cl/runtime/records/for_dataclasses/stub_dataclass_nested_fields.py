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
from stubs.cl.runtime.records.dataclasses.stub_dataclass_data import StubDataclassData
from stubs.cl.runtime.records.dataclasses.stub_dataclass_derived_data import StubDataclassDerivedData
from stubs.cl.runtime.records.dataclasses.stub_dataclass_derived_from_derived_data import (
    StubDataclassDerivedFromDerivedData,
)
from stubs.cl.runtime.records.dataclasses.stub_dataclass_nested_fields_key import StubDataclassNestedFieldsKey
from stubs.cl.runtime.records.dataclasses.stub_dataclass_record import StubDataclassRecord
from stubs.cl.runtime.records.dataclasses.stub_dataclass_record import StubDataclassRecordKey


@dataclass(slots=True, kw_only=True)
class StubDataclassNestedFields(StubDataclassNestedFieldsKey, RecordMixin[StubDataclassNestedFieldsKey]):
    """Stub derived class."""

    base_datafield: StubDataclassData = datafield(default_factory=StubDataclassData)
    """Stub field."""

    derived_datafield: StubDataclassDerivedData = datafield(default_factory=StubDataclassDerivedData)
    """Stub field."""

    derived_from_derived_datafield: StubDataclassDerivedFromDerivedData = datafield(
        default_factory=StubDataclassDerivedFromDerivedData
    )
    """Stub field."""

    polymorphic_datafield: StubDataclassData = datafield(default_factory=StubDataclassDerivedData)
    """Declared StubDataclassData but provided an instance of StubDataclassDerivedData."""

    polymorphic_derived_datafield: StubDataclassDerivedData = datafield(
        default_factory=StubDataclassDerivedFromDerivedData
    )
    """Declared StubDataclassDerivedData but provided an instance of StubDataclassDerivedFromDerivedData."""

    key_field: StubDataclassRecordKey = datafield(default_factory=lambda: StubDataclassRecordKey(id="uvw"))
    """Stub field."""

    record_as_key_field: StubDataclassRecordKey = datafield(default_factory=lambda: StubDataclassRecord())
    """Stub field with key type initialized to record type instance."""

    def get_key(self) -> StubDataclassNestedFieldsKey:
        return StubDataclassNestedFieldsKey(
            primitive=self.primitive, embedded_1=self.embedded_1, embedded_2=self.embedded_2
        )
