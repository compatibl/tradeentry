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
from typing import Dict, List, Optional
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.primitive.date_util import DateUtil
from stubs.cl.runtime.data.attrs.stub_attrs_record import StubAttrsRecord
from stubs.cl.runtime.data.attrs.stub_attrs_derived_record import StubAttrsDerivedRecord


def stub_dict_of_floats() -> Dict[str, float]:
    """Create stub values."""
    return {
        "Key0": 0.001,
        "Key1": 1.0,
        "Key2": 2.1,
        "Key3": 3.005,
        "Key4": 4.23,
        "Key5": 555.555
    }


def stub_dict_of_dates() -> Dict[str, dt.date]:
    """Create stub values."""
    return {
        "Key0": DateUtil.from_fields(2001, 1, 1),
        "Key1": DateUtil.from_fields(2001, 1, 10),
        "Key2": DateUtil.from_fields(2022, 5, 5),
        "Key3": DateUtil.from_fields(2008, 12, 12),
    }


def stub_dict_of_base_records() -> Dict[str, StubAttrsRecord]:
    """Create stub values."""
    return {
        "Key1": StubAttrsRecord(record_index=0, record_id='A'),
        "Key2": StubAttrsRecord(record_index=1, record_id='A'),
        "Key3": StubAttrsRecord(record_index=2, record_id='B'),
        "Key4": StubAttrsRecord(record_index=3, record_id='B'),
        "Key5": StubAttrsRecord(record_index=4, record_id='C'),
        "Key6": StubAttrsRecord(record_index=5, record_id='C'),
    }


def stub_dict_of_derived_records() -> Dict[str, StubAttrsDerivedRecord]:
    """Create stub values."""
    return {
        "Key0": StubAttrsDerivedRecord(record_index=0, record_id='A'),
        "Key1": StubAttrsDerivedRecord(record_index=1, record_id='A'),
        "Key2": StubAttrsDerivedRecord(record_index=2, record_id='B'),
        "Key3": StubAttrsDerivedRecord(record_index=3, record_id='B'),
        "Key4": StubAttrsDerivedRecord(record_index=4, record_id='C'),
        "Key5": StubAttrsDerivedRecord(record_index=5, record_id='C'),
    }

# TODO: Provide stub values for the dicts of lists


@attrs_record
class StubAttrsWithDictFields(StubAttrsRecord):
    """Stub record whose elements are dictionaries."""

    dict_of_floats: Optional[Dict[str, float]] = attrs_field(factory=stub_dict_of_floats)
    """Stub field."""
    
    dict_of_dates: Optional[Dict[str, dt.date]] = attrs_field(factory=stub_dict_of_dates)
    """Stub field."""

    dict_of_base_records: Optional[Dict[str, StubAttrsRecord]] = attrs_field(factory=stub_dict_of_base_records)
    """Stub field."""

    dict_of_derived_records: Optional[Dict[str, StubAttrsDerivedRecord]] = attrs_field(factory=stub_dict_of_derived_records)
    """Stub field."""

    dict_of_float_lists: Optional[Dict[str, List[float]]] = attrs_field()
    """Stub field."""
    
    dict_of_date_lists: Optional[Dict[str, List[dt.date]]] = attrs_field()
    """Stub field."""

    dict_of_base_record_lists: Optional[Dict[str, List[StubAttrsRecord]]] = attrs_field()
    """Stub field."""

    dict_of_derived_record_lists: Optional[Dict[str, List[StubAttrsDerivedRecord]]] = attrs_field()
    """Stub field."""

