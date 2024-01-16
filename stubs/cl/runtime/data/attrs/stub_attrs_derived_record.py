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
from typing import Dict, List, Optional
from cl.runtime.data.index_util import index_fields
from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.primitive.time_util import TimeUtil
from stubs.cl.runtime.data.attrs.stub_attrs_record import StubAttrsRecord, data_list_field_factory
from stubs.cl.runtime.data.attrs.stub_attrs_record_key import StubAttrsRecordKey
from stubs.cl.runtime.data.attrs.stub_attrs_derived_data import StubAttrsDerivedData
from stubs.cl.runtime.data.attrs.stub_attrs_derived_from_derived_data import StubAttrsDerivedFromDerivedData
from stubs.cl.runtime.data.attrs.stub_attrs_data import StubAttrsData
from stubs.cl.runtime.data.enum.stub_int_enum import StubIntEnum


@index_fields('derived_float_field, -float_field')
@attrs_record(init=False)
class StubAttrsDerivedRecord(StubAttrsRecord):
    """Stub derived class."""

    float_field: float = attrs_field(default=123.456)
    """Stub field."""

    date_field: dt.date = attrs_field(default=DateUtil.from_str("2023-05-01"))
    """Stub field."""

    enum_field: StubIntEnum = attrs_field(default=StubIntEnum.ENUM_VALUE_2)
    """Stub field."""

    time_field: dt.time = attrs_field(default=TimeUtil.from_str("10:15:00"))
    """Stub field."""

    date_time_field: dt.datetime = attrs_field(default=DateTimeUtil.from_str("2023-05-01T10:15:00"))
    """Stub field."""

    long_field: int = attrs_field(default=9007199254740991, subtype='long')
    """The default is maximum safe signed int for JSON: 2^53 - 1."""

    bytes_field: bytes = attrs_field(default=bytes([100, 110, 120]))
    """Stub field."""

    renamed_field: str = attrs_field(name='new_name')
    """Stub field where key in API is not the same as Python attribute name."""

    relabeled_field: str = attrs_field(label='New Label')
    """Stub field where label in UI is not the same as Python attribute name."""

    data_field: StubAttrsData = attrs_field(factory=StubAttrsData)
    """Stub field."""

    data_list_field: List[StubAttrsData] = attrs_field(factory=data_list_field_factory)
    """Stub field."""

    str_list: List[str] = attrs_field()
    """Stub field."""

    str_dict: Dict[str, str] = attrs_field()
    """Stub field."""

    float_list: List[float] = attrs_field()
    """Stub field."""

    float_dict: Dict[str, float] = attrs_field()
    """Stub field."""

    derived_data_field: StubAttrsDerivedData = attrs_field(factory=StubAttrsDerivedData)
    """Stub field."""

    derived_from_derived_data_field: StubAttrsDerivedFromDerivedData = attrs_field(default=StubAttrsDerivedFromDerivedData)
    """Stub field."""

    polymorphic_data_field: StubAttrsData = attrs_field(factory=StubAttrsDerivedData)
    """Declared StubAttrsData but provided an instance of StubAttrsDerivedData."""

    polymorphic_derived_data_field: StubAttrsDerivedData = attrs_field(default=StubAttrsDerivedFromDerivedData)
    """Declared StubAttrsDerivedData but provided an instance of StubAttrsDerivedFromDerivedData."""

    data_list: List[StubAttrsData] = attrs_field()
    """Stub field."""

    data_dict: Dict[str, StubAttrsData] = attrs_field()
    """Stub field."""

    key_field: StubAttrsRecordKey = attrs_field()
    """Stub field."""

    key_list: List[StubAttrsRecordKey] = attrs_field()
    """Stub field."""

    key_dict: Dict[str, StubAttrsRecordKey] = attrs_field()
    """Stub field."""

    def non_virtual_derived_handler(self) -> None:
        pass

    def virtual_base_handler(self) -> None:
        pass

    def mutual_handler(self) -> str:
        return 'child_method'

    def __init__(self, *,
                 str_field: str = 'abc',
                 int_field: int = 0,
                 version: int = 0
                 ):
        """Create StubAttrsDerivedRecord object filled with general data of different types."""

        self.str_field = str_field
        self.int_field = int_field
        self.version = version

        self.float_field = 300.0
        self.date_field = DateUtil.from_fields(2003, 5, 1)
        self.time_field = TimeUtil.from_fields(10, 15, 30)  # 10:15:30
        self.date_time_field = DateTimeUtil.from_fields(2003, 5, 1, 10, 15)  # 2003-05-01T10:15:00
        self.derived_str_field = ''
        self.derived_float_field = 200.0

        # lists
        self.str_list = ['A', 'B', 'C']
        self.float_list = [1.0, 2.0, 3.0]

        # dicts
        self.str_dict = {
            "A": "a",
            "B": "b",
            "C": "c",
        }
        self.float_dict = {
            "1.0": 1.0,
            "2.0": 2.0,
            "3.0": 3.0,
        }

        # Data element
        self.data_field = StubAttrsData(float_field_3=1.0, str_field_3='AA')

        # Derived data elements
        self.derived_data_field = StubAttrsDerivedData()
        self.derived_data_field.float_field_3 = 1.0
        self.derived_data_field.str_field_3 = 'A'
        self.derived_data_field.derived_float_field = 2.0
        self.derived_data_field.date_field = 'B'
        self.derived_from_derived_data_field = StubAttrsDerivedFromDerivedData()
        self.derived_from_derived_data_field.float_field_3 = 1.0
        self.derived_from_derived_data_field.str_field_3 = 'A'
        self.derived_from_derived_data_field.derived_float_field = 2.0
        self.derived_from_derived_data_field.date_field = 'B'
        self.derived_from_derived_data_field.derived_from_derived_float_field = 2.0
        self.derived_from_derived_data_field.derived_from_derived_str_field = 'B'

        # Polymorphic data elements
        self.polymorphic_data_field = StubAttrsDerivedData()
        self.polymorphic_data_field.float_field_3 = 1.0
        self.polymorphic_data_field.str_field_3 = 'A'
        self.polymorphic_data_field.float_field_4 = 2.0
        self.polymorphic_data_field.str_field_4 = 'B'
        self.polymorphic_derived_data_field = StubAttrsDerivedFromDerivedData()
        self.polymorphic_derived_data_field.float_field_3 = 1.0
        self.polymorphic_derived_data_field.str_field_3 = 'A'
        self.polymorphic_derived_data_field.float_field_4 = 2.0
        self.polymorphic_derived_data_field.str_field_4 = 'B'
        self.polymorphic_derived_data_field.float_field_5 = 2.0
        self.polymorphic_derived_data_field.str_field_5 = 'B'

        # Data element list
        self.data_list = [
            StubAttrsData(float_field_3=1.0, str_field_3='A0'),
            StubAttrsDerivedData(
                float_field_3=2.0,
                str_field_3='A1',
                float_field_4=3.0,
                str_field_4='A11',
            ),
        ]

        # Data element dict
        self.data_dict = {
            "E1": StubAttrsData(float_field_3=1.0, str_field_3='A0'),
            "E2": StubAttrsDerivedData(
                float_field_3=2.0,
                str_field_3='A1',
                float_field_4=3.0,
                str_field_4='A11',
            ),
        }

        # Key element
        self.key_field = StubAttrsRecordKey(str_field='BB', int_field=2)

        # Key element list
        self.key_list = [
            StubAttrsRecordKey(str_field='B0', int_field=3),
            StubAttrsRecordKey(str_field='B1', int_field=4),
        ]

        # Key element dict
        self.key_dict = {
            "KE1": StubAttrsRecordKey(str_field='B0', int_field=3),
            "KE2": StubAttrsRecordKey(str_field='B1', int_field=4),
        }
        base_sample = StubAttrsRecord(str_field='A0', int_field=0)
        self.dict_of_base_sample_list = {"A0": [base_sample]}

