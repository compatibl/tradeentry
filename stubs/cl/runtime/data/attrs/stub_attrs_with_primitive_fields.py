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

import datetime as dt
from cl.runtime.primitive.ordered_uid import OrderedUid
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.data.key import Key
from stubs.cl.runtime.data.attrs.stub_attrs_enum import StubAttrsEnum
from stubs.cl.runtime.data.attrs.stub_attrs_with_primitive_fields_key import StubAttrsWithPrimitiveFieldsKey


@attrs_record
class StubAttrsWithPrimitiveFields(StubAttrsWithPrimitiveFieldsKey):
    """Stub record whose elements are primitive types."""

    float_field: float = attrs_field()
    """Stub field."""

    bytes_field: bytes = attrs_field()
    """Stub field."""

    int_field: int = attrs_field()
    """Stub field."""

    long_field: int = attrs_field(subtype='long')
    """Stub field."""

    bool_field: bool = attrs_field()
    """Stub field."""

    string_field: str = attrs_field()
    """Stub field."""

    enum_field: StubAttrsEnum = attrs_field()
    """Stub field."""

    date_field: dt.date = attrs_field()
    """Stub field."""

    time_field: dt.time = attrs_field()
    """Stub field."""

    date_time_field: dt.datetime = attrs_field()
    """Stub field."""

    key_field: Key = attrs_field()
    """Stub field."""

    guid_field: OrderedUid = attrs_field()
    """Stub field."""
