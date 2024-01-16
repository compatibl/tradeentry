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
import datetime as dt
from typing import List, Optional
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_record import StubAttrsRecord
from stubs.cl.runtime.data.attrs.stub_attrs_derived_record import StubAttrsDerivedRecord


def stub_list_of_floats() -> List[float]:
    """Create stub values."""
    return [
        0.001,
        1.0,
        2.1,
        3.005,
        4.23,
        555.555
    ]


def stub_list_of_dates() -> List[dt.date]:
    """Create stub values."""
    return [
        DateUtil.from_fields(2001, 1, 1),
        DateUtil.from_fields(2001, 1, 10),
        DateUtil.from_fields(2022, 5, 5),
        DateUtil.from_fields(2008, 12, 12),
    ]


def stub_list_of_base_records() -> List[StubAttrsRecord]:
    """Create stub values."""
    return [
        StubAttrsRecord(record_index=0, record_id='A'),
        StubAttrsRecord(record_index=1, record_id='A'),
        StubAttrsRecord(record_index=2, record_id='B'),
        StubAttrsRecord(record_index=3, record_id='B'),
        StubAttrsRecord(record_index=4, record_id='C'),
        StubAttrsRecord(record_index=5, record_id='C'),
    ]


def stub_list_of_derived_records() -> List[StubAttrsDerivedRecord]:
    """Create stub values."""
    return [
        StubAttrsDerivedRecord(record_index=0, record_id='A'),
        StubAttrsDerivedRecord(record_index=1, record_id='A'),
        StubAttrsDerivedRecord(record_index=2, record_id='B'),
        StubAttrsDerivedRecord(record_index=3, record_id='B'),
        StubAttrsDerivedRecord(record_index=4, record_id='C'),
        StubAttrsDerivedRecord(record_index=5, record_id='C'),
    ]


@attrs_record
class StubAttrsWithListFields(StubAttrsRecord):

    list_of_floats: Optional[List[float]] = attrs_field(factory=stub_list_of_floats)
    """Stub field."""

    list_of_base_records: Optional[List[StubAttrsRecord]] = attrs_field(factory=stub_list_of_base_records)
    """Stub field."""

    list_of_derived_records: Optional[List[StubAttrsDerivedRecord]] = attrs_field(factory=stub_list_of_derived_records)
    """Stub field."""

    list_of_dates: Optional[List[dt.date]] = attrs_field(factory=stub_list_of_dates)
    """Stub field."""
