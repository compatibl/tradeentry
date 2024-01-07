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
from cl.runtime.data.attrs.stubs.stub_attrs_base_record import StubAttrsBaseRecord
from cl.runtime.data.attrs.stubs.stub_attrs_base_record_key import StubAttrsBaseRecordKey
from cl.runtime.data.attrs.stubs.stub_attrs_derived_data import StubAttrsDerivedData
from cl.runtime.data.attrs.stubs.stub_attrs_derived_from_derived_data import StubAttrsDerivedFromDerivedData
from cl.runtime.data.attrs.stubs.stub_attrs_base_data import StubAttrsBaseData


@index_fields('float_field_2, -float_field')
@attrs_record
class StubAttrsDerivedRecord(StubAttrsBaseRecord):
    """Stub derived class."""

    float_field_2: Optional[float] = attrs_field()
    """Stub field."""

    string_field_2: Optional[str] = attrs_field()
    """Stub field."""

    array_of_string: Optional[List[str]] = attrs_field()
    """Stub field."""

    list_of_string: Optional[List[str]] = attrs_field()
    """Stub field."""

    dict_of_string: Optional[Dict[str, str]] = attrs_field()
    """Stub field."""

    array_of_float: Optional[List[float]] = attrs_field()
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

    base_attrs_field: Optional[StubAttrsBaseData] = attrs_field()
    """Stub field."""

    derived_attrs_field: Optional[StubAttrsDerivedData] = attrs_field()
    """Stub field."""

    derived_from_derived_attrs_field: Optional[StubAttrsDerivedFromDerivedData] = attrs_field()
    """Stub field."""

    polymorphic_attrs_field_1: Optional[StubAttrsBaseData] = attrs_field()
    """Stub field."""

    polymorphic_attrs_field_2: Optional[StubAttrsBaseData] = attrs_field()
    """Stub field."""

    before_rename: Optional[StubAttrsBaseData] = attrs_field(name='AfterRename')
    """Stub field."""

    data_list_field: Optional[List[StubAttrsBaseData]] = attrs_field()
    """Stub field."""

    data_dict_field: Optional[Dict[str, StubAttrsBaseData]] = attrs_field()
    """Stub field."""

    key_field: Optional[StubAttrsBaseRecordKey] = attrs_field()
    """Stub field."""

    key_list_field: Optional[List[StubAttrsBaseRecordKey]] = attrs_field()
    """Stub field."""

    key_dict_field: Optional[Dict[str, StubAttrsBaseRecordKey]] = attrs_field()
    """Stub field."""

    dict_of_base_sample_list: Optional[Dict[str, List[StubAttrsBaseRecord]]] = attrs_field()
    """Stub field."""

    def non_virtual_derived_handler(self) -> None:
        pass

    def virtual_base_handler(self) -> None:
        pass

    def mutual_handler(self) -> str:
        return 'child_method'

    @staticmethod
    def create(*, record_index: int = 0, record_id: str = 'A', version: int = 0) -> StubAttrsDerivedRecord:
        """Create StubAttrsDerivedRecord object filled with general data of different types."""

        obj = StubAttrsDerivedRecord()
        obj.record_id = record_id
        obj.record_index = record_index
        obj.version = version

        obj.float_field = 300.0
        obj.date_field = DateUtil.from_fields(2003, 5, 1)
        obj.time_field = DateTimeUtil.from_fields(10, 15, 30)  # 10:15:30
        obj.date_time_field = DateUtil.from_fields(2003, 5, 1, 10, 15)  # 2003-05-01T10:15:00
        obj.string_field_2 = ''
        obj.float_field_2 = 200.0

        # lists
        obj.list_of_string = ['A', 'B', 'C']
        obj.list_of_float = [1.0, 2.0, 3.0]
        obj.list_of_nullable_float = [10.0, None, 30.0]

        # dicts
        obj.dict_of_string = {
            "A": "a",
            "B": "b",
            "C": "c",
        }
        obj.dict_of_float = {
            "1.0": 1.0,
            "2.0": 2.0,
            "3.0": 3.0,
        }
        obj.dict_of_nullable_float = {
            "10.0": 1.0,
            "20.0": None,
            "30.0": 30.0,
        }

        # Data element
        obj.base_attrs_field = StubAttrsBaseData(float_field_3=1.0, string_field_3='AA')

        # Derived data elements
        obj.derived_attrs_field = StubAttrsDerivedData()
        obj.derived_attrs_field.float_field_3 = 1.0
        obj.derived_attrs_field.string_field_3 = 'A'
        obj.derived_attrs_field.float_field_4 = 2.0
        obj.derived_attrs_field.string_field_4 = 'B'
        obj.derived_from_derived_attrs_field = StubAttrsDerivedFromDerivedData()
        obj.derived_from_derived_attrs_field.float_field_3 = 1.0
        obj.derived_from_derived_attrs_field.string_field_3 = 'A'
        obj.derived_from_derived_attrs_field.float_field_4 = 2.0
        obj.derived_from_derived_attrs_field.string_field_4 = 'B'
        obj.derived_from_derived_attrs_field.float_field_5 = 2.0
        obj.derived_from_derived_attrs_field.string_field_5 = 'B'

        # Polymorphic data elements
        obj.polymorphic_attrs_field_1 = StubAttrsDerivedData()
        obj.polymorphic_attrs_field_1.float_field_3 = 1.0
        obj.polymorphic_attrs_field_1.string_field_3 = 'A'
        obj.polymorphic_attrs_field_1.float_field_4 = 2.0
        obj.polymorphic_attrs_field_1.string_field_4 = 'B'
        obj.polymorphic_attrs_field_2 = StubAttrsDerivedFromDerivedData()
        obj.polymorphic_attrs_field_2.float_field_3 = 1.0
        obj.polymorphic_attrs_field_2.string_field_3 = 'A'
        obj.polymorphic_attrs_field_2.float_field_4 = 2.0
        obj.polymorphic_attrs_field_2.string_field_4 = 'B'
        obj.polymorphic_attrs_field_2.float_field_5 = 2.0
        obj.polymorphic_attrs_field_2.string_field_5 = 'B'

        # Data element list
        obj.data_list_field = [
            StubAttrsBaseData(float_field_3=1.0, string_field_3='A0'),
            StubAttrsDerivedData(
                float_field_3=2.0,
                string_field_3='A1',
                float_field_4=3.0,
                string_field_4='A11',
            ),
        ]

        # Data element dict
        obj.data_dict_field = {
            "E1": StubAttrsBaseData(float_field_3=1.0, string_field_3='A0'),
            "E2": StubAttrsDerivedData(
                float_field_3=2.0,
                string_field_3='A1',
                float_field_4=3.0,
                string_field_4='A11',
            ),
        }

        # Key element
        obj.key_field = StubAttrsBaseRecordKey(record_id='BB', record_index=2)

        # Key element list
        obj.key_list_field = [
            StubAttrsBaseRecordKey(record_id='B0', record_index=3),
            StubAttrsBaseRecordKey(record_id='B1', record_index=4),
        ]

        # Key element dict
        obj.key_dict_field = {
            "KE1": StubAttrsBaseRecordKey(record_id='B0', record_index=3),
            "KE2": StubAttrsBaseRecordKey(record_id='B1', record_index=4),
        }
        base_sample = StubAttrsBaseRecord.create(record_index=0, record_id='A0')
        obj.dict_of_base_sample_list = {"A0": [base_sample]}

        return obj
