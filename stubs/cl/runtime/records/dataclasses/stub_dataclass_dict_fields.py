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
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.primitive.date_util import DateUtil
from dataclasses import dataclass
from stubs.cl.runtime.records.dataclasses.stub_dataclass_data import StubDataclassData
from stubs.cl.runtime.records.dataclasses.stub_dataclass_derived_record import StubDataclassDerivedRecord
from stubs.cl.runtime.records.dataclasses.stub_dataclass_record import StubDataclassRecord
from stubs.cl.runtime.records.dataclasses.stub_dataclass_record import StubDataclassRecordKey
from typing import Dict


def stub_dataclass_str_dict_factory() -> Dict[str, str]:
    """Create stub values."""
    return {"a": "abc", "b": "def"}


def stub_dataclass_float_dict_factory() -> Dict[str, float]:
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
        "j": 12345.6789,
    }


def stub_dataclass_date_dict_factory() -> Dict[str, dt.date]:
    """Create stub values."""
    return {
        "a": DateUtil.from_fields(2003, 4, 21),
        "b": DateUtil.from_fields(2003, 5, 1),
    }


def stub_dataclass_data_dict_factory() -> Dict[str, StubDataclassData]:
    """Create stub values."""
    return {
        "a": StubDataclassData(str_field="A", int_field=1),
        "b": StubDataclassData(str_field="B", int_field=2),
    }


def stub_dataclass_key_dict_factory() -> Dict[str, StubDataclassRecordKey]:
    """Create stub values."""
    return {
        "a": (StubDataclassRecord, "A", 1),
        "b": (StubDataclassRecord, "B", 2),
    }


def stub_dataclass_record_dict_factory() -> Dict[str, StubDataclassRecord]:
    """Create stub values."""
    return {
        "a": StubDataclassRecord(str_field="A", int_field=1),
        "b": StubDataclassRecord(str_field="B", int_field=2),
    }


def stub_dataclass_derived_record_dict_factory() -> Dict[str, StubDataclassDerivedRecord]:
    """Create stub values."""
    return {
        "a": StubDataclassDerivedRecord(str_field="A", int_field=1),
        "b": StubDataclassDerivedRecord(str_field="B", int_field=2),
    }


@dataclass
class StubDataclassDictFields(StubDataclassRecord):
    """Stub record whose elements are dictionaries."""

    str_dict: Dict[str, str] = datafield(default_factory=stub_dataclass_str_dict_factory)
    """Stub field."""

    float_dict: Dict[str, float] = datafield(default_factory=stub_dataclass_float_dict_factory)
    """Stub field."""

    date_dict: Dict[str, dt.date] = datafield(default_factory=stub_dataclass_date_dict_factory)
    """Stub field."""

    data_dict: Dict[str, StubDataclassData] = datafield(default_factory=stub_dataclass_data_dict_factory)
    """Stub field."""

    key_dict: Dict[str, StubDataclassRecordKey] = datafield(default_factory=stub_dataclass_key_dict_factory)
    """Stub field."""

    record_dict: Dict[str, StubDataclassRecord] = datafield(default_factory=stub_dataclass_record_dict_factory)
    """Stub field."""

    derived_record_dict: Dict[str, StubDataclassDerivedRecord] = datafield(
        default_factory=stub_dataclass_derived_record_dict_factory
    )
    """Stub field."""
