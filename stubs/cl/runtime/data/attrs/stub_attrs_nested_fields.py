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
from cl.runtime.data.index_util import index_fields
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_nested_fields_key import StubAttrsNestedFieldsKey
from stubs.cl.runtime.data.attrs.stub_attrs_record_key import StubAttrsRecordKey
from stubs.cl.runtime.data.attrs.stub_attrs_derived_data import StubAttrsDerivedData
from stubs.cl.runtime.data.attrs.stub_attrs_derived_from_derived_data import StubAttrsDerivedFromDerivedData
from stubs.cl.runtime.data.attrs.stub_attrs_data import StubAttrsData


@index_fields('derived_float_field, -float_field')
@attrs_record(init=False)
class StubAttrsNestedFields(StubAttrsNestedFieldsKey):
    """Stub derived class."""

    data_field: StubAttrsData = attrs_field(factory=StubAttrsData)
    """Stub field."""

    key_field: StubAttrsRecordKey = attrs_field(factory=StubAttrsRecordKey)
    """Stub field."""

    derived_data_field: StubAttrsDerivedData = attrs_field(factory=StubAttrsDerivedData)
    """Stub field."""

    derived_from_derived_data_field: StubAttrsDerivedFromDerivedData = attrs_field(default=StubAttrsDerivedFromDerivedData)
    """Stub field."""

    polymorphic_data_field: StubAttrsData = attrs_field(factory=StubAttrsDerivedData)
    """Declared StubAttrsData but provided an instance of StubAttrsDerivedData."""

    polymorphic_derived_data_field: StubAttrsDerivedData = attrs_field(default=StubAttrsDerivedFromDerivedData)
    """Declared StubAttrsDerivedData but provided an instance of StubAttrsDerivedFromDerivedData."""


