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
from dataclasses import dataclass
from cl.runtime.classes.dataclasses.dataclass_fields import data_field
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_data import StubDataclassData
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_derived_record import StubDataclassDerivedRecord
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_list_fields import stub_dataclass_data_list_factory
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_list_fields import stub_dataclass_date_list_factory
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_list_fields import stub_dataclass_derived_record_list_factory
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_list_fields import stub_dataclass_float_list_factory
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_list_fields import stub_dataclass_key_list_factory
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_list_fields import stub_dataclass_record_list_factory
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_list_fields import stub_dataclass_str_list_factory
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_record import StubDataclassRecord
from stubs.cl.runtime.classes.dataclasses.stub_dataclass_record import StubDataclassRecordKey
from typing import Dict
from typing import List


def stub_dataclass_str_list_dict_factory() -> Dict[str, List[str]]:
    """Create stub values."""
    return {
        "a": stub_dataclass_str_list_factory(),
        "b": stub_dataclass_str_list_factory(),
    }


def stub_dataclass_float_list_dict_factory() -> Dict[str, List[float]]:
    """Create stub values."""
    return {
        "a": stub_dataclass_float_list_factory(),
        "b": stub_dataclass_float_list_factory(),
    }


def stub_dataclass_date_list_dict_factory() -> Dict[str, List[dt.date]]:
    """Create stub values."""
    return {
        "a": stub_dataclass_date_list_factory(),
        "b": stub_dataclass_date_list_factory(),
    }


def stub_dataclass_data_list_dict_factory() -> Dict[str, List[StubDataclassData]]:
    """Create stub values."""
    return {
        "a": stub_dataclass_data_list_factory(),
        "b": stub_dataclass_data_list_factory(),
    }


def stub_dataclass_key_list_dict_factory() -> Dict[str, List[StubDataclassRecordKey]]:
    """Create stub values."""
    return {
        "a": stub_dataclass_key_list_factory(),
        "b": stub_dataclass_key_list_factory(),
    }


def stub_dataclass_record_list_dict_factory() -> Dict[str, List[StubDataclassRecord]]:
    """Create stub values."""
    return {
        "a": stub_dataclass_record_list_factory(),
        "b": stub_dataclass_record_list_factory(),
    }


def stub_dataclass_derived_record_list_dict_factory() -> Dict[str, List[StubDataclassDerivedRecord]]:
    """Create stub values."""
    return {
        "a": stub_dataclass_derived_record_list_factory(),
        "b": stub_dataclass_derived_record_list_factory(),
    }


@dataclass
class StubDataclassListDictFields(StubDataclassRecord):
    """Stub record whose elements are dictionaries."""

    float_list_dict: Dict[str, List[float]] = data_field(default_factory=stub_dataclass_float_list_dict_factory)
    """Stub field."""

    date_list_dict: Dict[str, List[dt.date]] = data_field(default_factory=stub_dataclass_date_list_dict_factory)
    """Stub field."""

    record_list_dict: Dict[str, List[StubDataclassRecord]] = data_field(default_factory=stub_dataclass_record_list_dict_factory)
    """Stub field."""

    derived_record_list_dict: Dict[str, List[StubDataclassDerivedRecord]] = data_field(
        default_factory=stub_dataclass_derived_record_list_dict_factory
    )
    """Stub field."""
