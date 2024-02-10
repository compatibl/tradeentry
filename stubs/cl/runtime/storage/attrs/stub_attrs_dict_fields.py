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
from typing import Dict, List
from cl.runtime.storage.attrs import data_field, data_class
from cl.runtime.primitive.date_util import DateUtil
from stubs.cl.runtime.storage.attrs.stub_attrs_data import StubAttrsData
from stubs.cl.runtime.storage.attrs.stub_attrs_record import StubAttrsRecord
from stubs.cl.runtime.storage.attrs.stub_attrs_derived_record import StubAttrsDerivedRecord
from stubs.cl.runtime.storage.attrs.stub_attrs_record_key import StubAttrsRecordKey


def stub_attrs_str_dict_factory() -> Dict[str, str]:
    """Create stub values."""
    return {
        "a": "abc",
        "b": "def"
    }


def stub_attrs_float_dict_factory() -> Dict[str, float]:
    """Create stub values."""
    return {
        "a": 0.0000123456789,
        "b": 0.000123456789,
        "c": 0.00123456789,
        "d": 0.0123456789,
        "e": 0.123456789,
        "f": 1.23456789,
        "g": 12.3456789,
        "h": 123.456789,
        "i": 1234.56789,
        "j": 12345.6789
    }


def stub_attrs_date_dict_factory() -> Dict[str, dt.date]:
    """Create stub values."""
    return {
        "a": DateUtil.from_fields(2003, 4, 21),
        "b": DateUtil.from_fields(2003, 5, 1),
    }


def stub_attrs_data_dict_factory() -> Dict[str, StubAttrsData]:
    """Create stub values."""
    return {
        "a": StubAttrsData(str_field='A', int_field=1),
        "b": StubAttrsData(str_field='B', int_field=2),
    }


def stub_attrs_key_dict_factory() -> Dict[str, StubAttrsRecordKey]:
    """Create stub values."""
    return {
        "a": StubAttrsRecordKey(str_field='A', int_field=1),
        "b": StubAttrsRecordKey(str_field='B', int_field=2),
    }


def stub_attrs_record_dict_factory() -> Dict[str, StubAttrsRecord]:
    """Create stub values."""
    return {
        "a": StubAttrsRecord(str_field='A', int_field=1),
        "b": StubAttrsRecord(str_field='B', int_field=2),
    }


def stub_attrs_derived_record_dict_factory() -> Dict[str, StubAttrsDerivedRecord]:
    """Create stub values."""
    return {
        "a": StubAttrsDerivedRecord(str_field='A', int_field=1),
        "b": StubAttrsDerivedRecord(str_field='B', int_field=2),
    }


@data_class
class StubAttrsDictFields(StubAttrsRecord):
    """Stub record whose elements are dictionaries."""

    str_dict: Dict[str, str] = data_field(factory=stub_attrs_str_dict_factory)
    """Stub field."""

    float_dict: Dict[str, float] = data_field(factory=stub_attrs_float_dict_factory)
    """Stub field."""
    
    date_dict: Dict[str, dt.date] = data_field(factory=stub_attrs_date_dict_factory)
    """Stub field."""

    data_dict: Dict[str, StubAttrsData] = data_field(factory=stub_attrs_data_dict_factory)
    """Stub field."""

    key_dict: Dict[str, StubAttrsRecordKey] = data_field(factory=stub_attrs_key_dict_factory)
    """Stub field."""

    record_dict: Dict[str, StubAttrsRecord] = data_field(factory=stub_attrs_record_dict_factory)
    """Stub field."""

    derived_record_dict: Dict[str, StubAttrsDerivedRecord] = data_field(factory=stub_attrs_derived_record_dict_factory)
    """Stub field."""
