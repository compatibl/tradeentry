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
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_data import StubAttrsData
from stubs.cl.runtime.data.attrs.stub_attrs_list_fields import stub_attrs_str_list_factory, \
    stub_attrs_float_list_factory, stub_attrs_date_list_factory, stub_attrs_data_list_factory, \
    stub_attrs_key_list_factory, stub_attrs_record_list_factory, stub_attrs_derived_record_list_factory
from stubs.cl.runtime.data.attrs.stub_attrs_record import StubAttrsRecord
from stubs.cl.runtime.data.attrs.stub_attrs_derived_record import StubAttrsDerivedRecord
from stubs.cl.runtime.data.attrs.stub_attrs_record_key import StubAttrsRecordKey


def stub_attrs_str_list_dict_factory() -> Dict[str, List[str]]:
    """Create stub values."""
    return {
        "a": stub_attrs_str_list_factory(),
        "b": stub_attrs_str_list_factory(),
    }


def stub_attrs_float_list_dict_factory() -> Dict[str, List[float]]:
    """Create stub values."""
    return {
        "a": stub_attrs_float_list_factory(),
        "b": stub_attrs_float_list_factory(),
    }


def stub_attrs_date_list_dict_factory() -> Dict[str, List[dt.date]]:
    """Create stub values."""
    return {
        "a": stub_attrs_date_list_factory(),
        "b": stub_attrs_date_list_factory(),
    }


def stub_attrs_data_list_dict_factory() -> Dict[str, List[StubAttrsData]]:
    """Create stub values."""
    return {
        "a": stub_attrs_data_list_factory(),
        "b": stub_attrs_data_list_factory(),
    }


def stub_attrs_key_list_dict_factory() -> Dict[str, List[StubAttrsRecordKey]]:
    """Create stub values."""
    return {
        "a": stub_attrs_key_list_factory(),
        "b": stub_attrs_key_list_factory(),
    }


def stub_attrs_record_list_dict_factory() -> Dict[str, List[StubAttrsRecord]]:
    """Create stub values."""
    return {
        "a": stub_attrs_record_list_factory(),
        "b": stub_attrs_record_list_factory(),
    }


def stub_attrs_derived_record_list_dict_factory() -> Dict[str, List[StubAttrsDerivedRecord]]:
    """Create stub values."""
    return {
        "a": stub_attrs_derived_record_list_factory(),
        "b": stub_attrs_derived_record_list_factory(),
    }


@attrs_record
class StubAttrsDictFields(StubAttrsRecord):
    """Stub record whose elements are dictionaries."""

    float_list_dict: Dict[str, List[float]] = attrs_field(factory=stub_attrs_float_list_dict_factory)
    """Stub field."""
    
    date_list_dict: Dict[str, List[dt.date]] = attrs_field(factory=stub_attrs_date_list_dict_factory)
    """Stub field."""

    record_list_dict: Dict[str, List[StubAttrsRecord]] = attrs_field(factory=stub_attrs_record_list_dict_factory)
    """Stub field."""

    derived_record_list_dict: Dict[str, List[StubAttrsDerivedRecord]] = attrs_field(factory=stub_attrs_derived_record_list_dict_factory)
    """Stub field."""
