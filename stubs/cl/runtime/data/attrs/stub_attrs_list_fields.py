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


def stub_float_list() -> List[float]:
    """Create stub values."""
    return [
        0.0000123456789,
        0.000123456789,
        0.00123456789,
        0.0123456789,
        0.123456789,
        1.23456789,
        12.3456789,
        123.456789,
        1234.56789,
        12345.6789
    ]


def stub_date_list() -> List[dt.date]:
    """Create stub values."""
    return [
        DateUtil.from_fields(2003, 4, 21),
        DateUtil.from_fields(2003, 5, 1),
    ]


def stub_record_list() -> List[StubAttrsRecord]:
    """Create stub values."""
    return [
        StubAttrsRecord(str_field='A', int_field=0),
        StubAttrsRecord(str_field='B', int_field=1),
    ]


def stub_derived_record_list() -> List[StubAttrsDerivedRecord]:
    """Create stub values."""
    return [
        StubAttrsDerivedRecord(str_field='A', int_field=0),
        StubAttrsDerivedRecord(str_field='B', int_field=1),
    ]


@attrs_record
class StubAttrsListFields(StubAttrsRecord):

    float_list: List[float] = attrs_field(factory=stub_float_list)
    """Stub field."""

    date_list: List[dt.date] = attrs_field(factory=stub_date_list)
    """Stub field."""

    record_list: List[StubAttrsRecord] = attrs_field(factory=stub_record_list)
    """Stub field."""

    derived_record_list: List[StubAttrsDerivedRecord] = attrs_field(factory=stub_derived_record_list)
    """Stub field."""

