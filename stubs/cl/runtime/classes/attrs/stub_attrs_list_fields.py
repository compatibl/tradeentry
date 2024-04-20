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
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.classes.attrs_util import data_class
from cl.runtime.classes.attrs_util import data_field
from stubs.cl.runtime.classes.attrs.stub_attrs_data import StubAttrsData
from stubs.cl.runtime.classes.attrs.stub_attrs_derived_record import StubAttrsDerivedRecord
from stubs.cl.runtime.classes.attrs.stub_attrs_record import StubAttrsRecord
from stubs.cl.runtime.classes.attrs.stub_attrs_record import StubAttrsRecordKey
from typing import List


def stub_attrs_str_list_factory() -> List[str]:
    """Create stub values."""
    return ["abc", "def"]


def stub_attrs_float_list_factory() -> List[float]:
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
        12345.6789,
    ]


def stub_attrs_date_list_factory() -> List[dt.date]:
    """Create stub values."""
    return [
        DateUtil.from_fields(2003, 4, 21),
        DateUtil.from_fields(2003, 5, 1),
    ]


def stub_attrs_data_list_factory() -> List[StubAttrsData]:
    """Create stub values."""
    return [
        StubAttrsData(str_field="A", int_field=0),
        StubAttrsData(str_field="B", int_field=1),
    ]


def stub_attrs_key_list_factory() -> List[StubAttrsRecordKey]:
    """Create stub values."""
    return [
        (StubAttrsRecord, "A", 0),
        (StubAttrsRecord, "B", 1),
    ]


def stub_attrs_record_list_factory() -> List[StubAttrsRecord]:
    """Create stub values."""
    return [
        StubAttrsRecord(str_field="A", int_field=0),
        StubAttrsRecord(str_field="B", int_field=1),
    ]


def stub_attrs_derived_record_list_factory() -> List[StubAttrsDerivedRecord]:
    """Create stub values."""
    return [
        StubAttrsDerivedRecord(str_field="A", int_field=0),
        StubAttrsDerivedRecord(str_field="B", int_field=1),
    ]


@data_class
class StubAttrsListFields(StubAttrsRecord):
    str_list: List[str] = data_field(factory=stub_attrs_str_list_factory)
    """Stub field."""

    float_list: List[float] = data_field(factory=stub_attrs_float_list_factory)
    """Stub field."""

    date_list: List[dt.date] = data_field(factory=stub_attrs_date_list_factory)
    """Stub field."""

    data_list: List[StubAttrsData] = data_field(factory=stub_attrs_data_list_factory)
    """Stub field."""

    key_list: List[StubAttrsRecordKey] = data_field(factory=stub_attrs_key_list_factory)
    """Stub field."""

    record_list: List[StubAttrsRecord] = data_field(factory=stub_attrs_record_list_factory)
    """Stub field."""

    derived_record_list: List[StubAttrsDerivedRecord] = data_field(factory=stub_attrs_derived_record_list_factory)
    """Stub field."""
