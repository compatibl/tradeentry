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
from cl.runtime.storage.index_util import index_fields
from cl.runtime.storage.attrs import data_field, data_class
from stubs.cl.runtime.storage.attrs.stub_attrs_nested_fields_key import StubAttrsNestedFieldsKey
from stubs.cl.runtime.storage.attrs.stub_attrs_record import StubAttrsRecord
from stubs.cl.runtime.storage.attrs.stub_attrs_record_key import StubAttrsRecordKey
from stubs.cl.runtime.storage.attrs.stub_attrs_derived_data import StubAttrsDerivedData
from stubs.cl.runtime.storage.attrs.stub_attrs_derived_from_derived_data import StubAttrsDerivedFromDerivedData
from stubs.cl.runtime.storage.attrs.stub_attrs_data import StubAttrsData


@index_fields('derived_float_field, -float_field')
@data_class(init=False)
class StubAttrsNestedFields(StubAttrsNestedFieldsKey):
    """Stub derived class."""

    data_field: StubAttrsData = data_field(factory=StubAttrsData)
    """Stub field."""

    derived_data_field: StubAttrsDerivedData = data_field(factory=StubAttrsDerivedData)
    """Stub field."""

    derived_from_derived_data_field: StubAttrsDerivedFromDerivedData = data_field(default=StubAttrsDerivedFromDerivedData)
    """Stub field."""

    polymorphic_data_field: StubAttrsData = data_field(factory=StubAttrsDerivedData)
    """Declared StubAttrsData but provided an instance of StubAttrsDerivedData."""

    polymorphic_derived_data_field: StubAttrsDerivedData = data_field(default=StubAttrsDerivedFromDerivedData)
    """Declared StubAttrsDerivedData but provided an instance of StubAttrsDerivedFromDerivedData."""

    key_field: StubAttrsRecordKey = data_field(factory=StubAttrsRecordKey)
    """Stub field."""

    record_as_key_field: StubAttrsRecordKey = data_field(factory=StubAttrsRecord)
    """Stub field with key type initialized to record type instance."""


