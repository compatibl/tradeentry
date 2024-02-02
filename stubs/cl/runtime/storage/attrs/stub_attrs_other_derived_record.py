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
from cl.runtime.storage.index_util import index_fields
from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.storage.attrs_record_util import attrs_record
from cl.runtime.storage.attrs_field_util import attrs_field
from stubs.cl.runtime.storage.attrs.stub_attrs_record import StubAttrsRecord


@index_fields('other_float_field, other_str_field, -int_field')
@attrs_record
class StubAttrsOtherDerivedRecord(StubAttrsRecord):
    """Another type derived from StubAttrsRecord."""

    other_derived: str = attrs_field(default='other_derived')
    """Stub field for other derived class."""



