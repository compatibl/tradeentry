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
from typing import Dict, List, Optional
from cl.runtime.data.index_util import index_fields
from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.primitive.time_util import TimeUtil
from stubs.cl.runtime.data.attrs.stub_attrs_record import StubAttrsRecord
from stubs.cl.runtime.data.attrs.stub_attrs_record_key import StubAttrsRecordKey
from stubs.cl.runtime.data.attrs.stub_attrs_derived_data import StubAttrsDerivedData
from stubs.cl.runtime.data.attrs.stub_attrs_derived_from_derived_data import StubAttrsDerivedFromDerivedData
from stubs.cl.runtime.data.attrs.stub_attrs_data import StubAttrsData


@index_fields('derived_float_field, -float_field')
@attrs_record(init=False)
class StubAttrsDerivedRecord(StubAttrsRecord):
    """Stub derived class."""

    derived_float_field: Optional[float] = attrs_field()
    """Stub field."""

    derived_string_field: Optional[str] = attrs_field()
    """Stub field."""

    derived_string_list_field: Optional[List[str]] = attrs_field()
    """Stub field."""

    derived_string_dict_field: Optional[Dict[str, str]] = attrs_field()
    """Stub field."""

    array_of_nullable_float: Optional[List[float]] = attrs_field()
    """Stub field."""

    list_of_float: Optional[List[float]] = attrs_field()
    """Stub field."""

    list_of_nullable_float: Optional[List[float]] = attrs_field()
    """Stub field."""

    dict_of_float: Optional[Dict[str, float]] = attrs_field()
    """Stub field."""

    dict_of_nullable_float: Optional[Dict[str, float]] = attrs_field()
    """Stub field."""

    base_attrs_field: Optional[StubAttrsData] = attrs_field()
    """Stub field."""

    derived_attrs_field: Optional[StubAttrsDerivedData] = attrs_field()
    """Stub field."""

    derived_from_derived_attrs_field: Optional[StubAttrsDerivedFromDerivedData] = attrs_field()
    """Stub field."""

    polymorphic_attrs_field_1: Optional[StubAttrsData] = attrs_field()
    """Stub field."""

    polymorphic_attrs_field_2: Optional[StubAttrsData] = attrs_field()
    """Stub field."""

    before_rename: Optional[StubAttrsData] = attrs_field(name='AfterRename')
    """Stub field."""

    data_list_field: Optional[List[StubAttrsData]] = attrs_field()
    """Stub field."""

    data_dict_field: Optional[Dict[str, StubAttrsData]] = attrs_field()
    """Stub field."""

    key_field: Optional[StubAttrsRecordKey] = attrs_field()
    """Stub field."""

    key_list_field: Optional[List[StubAttrsRecordKey]] = attrs_field()
    """Stub field."""

    key_dict_field: Optional[Dict[str, StubAttrsRecordKey]] = attrs_field()
    """Stub field."""

    dict_of_base_sample_list: Optional[Dict[str, List[StubAttrsRecord]]] = attrs_field()
    """Stub field."""

    def non_virtual_derived_handler(self) -> None:
        pass

    def virtual_base_handler(self) -> None:
        pass

    def mutual_handler(self) -> str:
        return 'child_method'

    def __init__(self, *,
                 record_id: str = 'abc',
                 record_index: int = 0,
                 version: int = 0
                 ):
        """Create StubAttrsDerivedRecord object filled with general data of different types."""

        self.record_id = record_id
        self.record_index = record_index
        self.version = version

        self.float_field = 300.0
        self.date_field = DateUtil.from_fields(2003, 5, 1)
        self.time_field = TimeUtil.from_fields(10, 15, 30)  # 10:15:30
        self.date_time_field = DateTimeUtil.from_fields(2003, 5, 1, 10, 15)  # 2003-05-01T10:15:00
        self.derived_string_field = ''
        self.derived_float_field = 200.0

        # lists
        self.derived_string_list_field = ['A', 'B', 'C']
        self.list_of_float = [1.0, 2.0, 3.0]
        self.list_of_nullable_float = [10.0, None, 30.0]

        # dicts
        self.derived_string_dict_field = {
            "A": "a",
            "B": "b",
            "C": "c",
        }
        self.dict_of_float = {
            "1.0": 1.0,
            "2.0": 2.0,
            "3.0": 3.0,
        }
        self.dict_of_nullable_float = {
            "10.0": 1.0,
            "20.0": None,
            "30.0": 30.0,
        }

        # Data element
        self.base_attrs_field = StubAttrsData(float_field_3=1.0, string_field_3='AA')

        # Derived data elements
        self.derived_attrs_field = StubAttrsDerivedData()
        self.derived_attrs_field.float_field_3 = 1.0
        self.derived_attrs_field.string_field_3 = 'A'
        self.derived_attrs_field.derived_float_field = 2.0
        self.derived_attrs_field.derived_string_field = 'B'
        self.derived_from_derived_attrs_field = StubAttrsDerivedFromDerivedData()
        self.derived_from_derived_attrs_field.float_field_3 = 1.0
        self.derived_from_derived_attrs_field.string_field_3 = 'A'
        self.derived_from_derived_attrs_field.derived_float_field = 2.0
        self.derived_from_derived_attrs_field.derived_string_field = 'B'
        self.derived_from_derived_attrs_field.derived_from_derived_float_field = 2.0
        self.derived_from_derived_attrs_field.derived_from_derived_str_field = 'B'

        # Polymorphic data elements
        self.polymorphic_attrs_field_1 = StubAttrsDerivedData()
        self.polymorphic_attrs_field_1.float_field_3 = 1.0
        self.polymorphic_attrs_field_1.string_field_3 = 'A'
        self.polymorphic_attrs_field_1.float_field_4 = 2.0
        self.polymorphic_attrs_field_1.string_field_4 = 'B'
        self.polymorphic_attrs_field_2 = StubAttrsDerivedFromDerivedData()
        self.polymorphic_attrs_field_2.float_field_3 = 1.0
        self.polymorphic_attrs_field_2.string_field_3 = 'A'
        self.polymorphic_attrs_field_2.float_field_4 = 2.0
        self.polymorphic_attrs_field_2.string_field_4 = 'B'
        self.polymorphic_attrs_field_2.float_field_5 = 2.0
        self.polymorphic_attrs_field_2.string_field_5 = 'B'

        # Data element list
        self.data_list_field = [
            StubAttrsData(float_field_3=1.0, string_field_3='A0'),
            StubAttrsDerivedData(
                float_field_3=2.0,
                string_field_3='A1',
                float_field_4=3.0,
                string_field_4='A11',
            ),
        ]

        # Data element dict
        self.data_dict_field = {
            "E1": StubAttrsData(float_field_3=1.0, string_field_3='A0'),
            "E2": StubAttrsDerivedData(
                float_field_3=2.0,
                string_field_3='A1',
                float_field_4=3.0,
                string_field_4='A11',
            ),
        }

        # Key element
        self.key_field = StubAttrsRecordKey(record_id='BB', record_index=2)

        # Key element list
        self.key_list_field = [
            StubAttrsRecordKey(record_id='B0', record_index=3),
            StubAttrsRecordKey(record_id='B1', record_index=4),
        ]

        # Key element dict
        self.key_dict_field = {
            "KE1": StubAttrsRecordKey(record_id='B0', record_index=3),
            "KE2": StubAttrsRecordKey(record_id='B1', record_index=4),
        }
        base_sample = StubAttrsRecord(record_index=0, record_id='A0')
        self.dict_of_base_sample_list = {"A0": [base_sample]}

