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
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from dataclasses import dataclass
from stubs.cl.runtime.records.dataclasses.stub_dataclass_data import StubDataclassData
from stubs.cl.runtime.records.dataclasses.stub_dataclass_derived_data import StubDataclassDerivedData
from stubs.cl.runtime.records.dataclasses.stub_dataclass_derived_from_derived_data import (
    StubDataclassDerivedFromDerivedData,
)
from stubs.cl.runtime.records.dataclasses.stub_dataclass_nested_fields_key import StubDataclassNestedFieldsKey, \
    StubDataclassNestedFieldsTable
from stubs.cl.runtime.records.dataclasses.stub_dataclass_record import StubDataclassRecord
from stubs.cl.runtime.records.dataclasses.stub_dataclass_record import StubDataclassRecordKey
from typing import Tuple
from typing import Type


@dataclass(slots=True, kw_only=True)
class StubDataclassNestedFields(DataclassMixin):
    """Stub derived class."""

    primitive: str = datafield(default="abc")
    """String key element."""

    embedded_1: StubDataclassRecordKey = datafield(default_factory=StubDataclassRecordKey)
    """Embedded key 1."""

    embedded_2: StubDataclassRecordKey = datafield(default_factory=StubDataclassRecordKey)
    """Embedded key 2."""

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

    key_field: StubDataclassRecordKey = datafield(default_factory=StubDataclassRecordKey)
    """Stub field."""

    record_as_key_field: StubDataclassRecordKey = datafield(default_factory=lambda: StubDataclassRecord())
    """Stub field with key type initialized to record type instance."""

    def get_key(self) -> StubDataclassNestedFieldsKey:
        return StubDataclassNestedFieldsTable, self.primitive, self.embedded_1, self.embedded_2
