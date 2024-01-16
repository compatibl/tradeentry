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


def stub_float_dict_field() -> Dict[str, float]:
    """Create stub values."""
    return {
        "Key0": 0.001,
        "Key1": 1.0,
        "Key2": 2.1,
        "Key3": 3.005,
        "Key4": 4.23,
        "Key5": 555.555
    }


def stub_date_dict_field() -> Dict[str, dt.date]:
    """Create stub values."""
    return {
        "A": DateUtil.from_fields(2003, 4, 21),
        "B": DateUtil.from_fields(2003, 5, 1),
    }


def stub_record_dict_field() -> Dict[str, StubAttrsRecord]:
    """Create stub values."""
    return {
        "A": StubAttrsRecord(record_id='A', record_index=1),
        "B": StubAttrsRecord(record_id='B', record_index=2),
    }


def stub_derived_record_dict_field() -> Dict[str, StubAttrsDerivedRecord]:
    """Create stub values."""
    return {
        "A": StubAttrsDerivedRecord(record_id='A', record_index=1),
        "B": StubAttrsDerivedRecord(record_id='B', record_index=2),
    }

# TODO: Provide stub values for the dicts of lists


@attrs_record
class StubAttrsDictFields(StubAttrsRecord):
    """Stub record whose elements are dictionaries."""

    float_dict_field: Optional[Dict[str, float]] = attrs_field(factory=stub_float_dict_field)
    """Stub field."""
    
    date_dict_field: Optional[Dict[str, dt.date]] = attrs_field(factory=stub_date_dict_field)
    """Stub field."""

    record_dict_field: Optional[Dict[str, StubAttrsRecord]] = attrs_field(factory=stub_record_dict_field)
    """Stub field."""

    derived_record_dict_field: Optional[Dict[str, StubAttrsDerivedRecord]] = attrs_field(factory=stub_derived_record_dict_field)
    """Stub field."""

    float_list_dict_field: Optional[Dict[str, List[float]]] = attrs_field()
    """Stub field."""
    
    date_list_dict_field: Optional[Dict[str, List[dt.date]]] = attrs_field()
    """Stub field."""

    record_list_dict_field: Optional[Dict[str, List[StubAttrsRecord]]] = attrs_field()
    """Stub field."""

    derived_record_list_dict_field: Optional[Dict[str, List[StubAttrsDerivedRecord]]] = attrs_field()
    """Stub field."""
