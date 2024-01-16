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
from typing import Optional
from cl.runtime.data.index_util import index_fields
from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_record import StubAttrsRecord


@index_fields('other_float_field_2, other_string_field_2, -record_index')
@attrs_record
class StubAttrsOtherDerivedRecord(StubAttrsRecord):
    """Another type derived from StubAttrsRecord."""

    other_string_field_2: Optional[str] = attrs_field(default='abc')
    """Stub field."""

    other_float_field_2: Optional[float] = attrs_field(default=200.0)
    """Stub field."""


