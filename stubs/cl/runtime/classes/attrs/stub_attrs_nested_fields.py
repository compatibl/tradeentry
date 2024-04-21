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
from typing import Tuple, Type

from cl.runtime.classes.dataclasses.dataclass_fields import data_field
from cl.runtime.classes.dataclasses.dataclass_mixin import DataclassMixin
from cl.runtime.storage.index_util import index_fields
from stubs.cl.runtime.classes.attrs.stub_attrs_data import StubAttrsData
from stubs.cl.runtime.classes.attrs.stub_attrs_derived_data import StubAttrsDerivedData
from stubs.cl.runtime.classes.attrs.stub_attrs_derived_from_derived_data import StubAttrsDerivedFromDerivedData
from stubs.cl.runtime.classes.attrs.stub_attrs_record import StubAttrsRecord
from stubs.cl.runtime.classes.attrs.stub_attrs_record import StubAttrsRecordKey

StubAttrsNestedFieldsKey = Tuple[Type['StubAttrsNestedFields'], str, StubAttrsRecordKey, StubAttrsRecordKey]


# @index_fields("derived_float_field, -float_field") # TODO: index_fields
@dataclass(init=False)
class StubAttrsNestedFields(DataclassMixin):
    """Stub derived class."""

    primitive: str = data_field(default="abc")
    """String key element."""

    embedded_1: StubAttrsRecordKey = data_field(default_factory=StubAttrsRecordKey)
    """Embedded key 1."""

    embedded_2: StubAttrsRecordKey = data_field(default_factory=StubAttrsRecordKey)
    """Embedded key 2."""

    base_data_field: StubAttrsData = data_field(default_factory=StubAttrsData)
    """Stub field."""

    derived_data_field: StubAttrsDerivedData = data_field(default_factory=StubAttrsDerivedData)
    """Stub field."""

    derived_from_derived_data_field: StubAttrsDerivedFromDerivedData = data_field(
        default=StubAttrsDerivedFromDerivedData
    )
    """Stub field."""

    polymorphic_data_field: StubAttrsData = data_field(default_factory=StubAttrsDerivedData)
    """Declared StubAttrsData but provided an instance of StubAttrsDerivedData."""

    polymorphic_derived_data_field: StubAttrsDerivedData = data_field(default=StubAttrsDerivedFromDerivedData)
    """Declared StubAttrsDerivedData but provided an instance of StubAttrsDerivedFromDerivedData."""

    key_field: StubAttrsRecordKey = data_field(default_factory=StubAttrsRecordKey)
    """Stub field."""

    record_as_key_field: StubAttrsRecordKey = data_field(default_factory=lambda: StubAttrsRecord())
    """Stub field with key type initialized to record type instance."""

    def get_key(self) -> StubAttrsNestedFieldsKey:
        return StubAttrsNestedFields, self.primitive, self.embedded_1, self.embedded_2
