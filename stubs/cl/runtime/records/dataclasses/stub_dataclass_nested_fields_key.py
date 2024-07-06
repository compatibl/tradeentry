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

from dataclasses import dataclass
from typing import Tuple, Type
from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield
from cl.runtime.records.dataclasses.dataclass_key_mixin import DataclassKeyMixin
from stubs.cl.runtime.records.dataclasses.stub_dataclass_record import StubDataclassRecordKey


@dataclass(slots=True)
class StubDataclassNestedFieldsKey(DataclassKeyMixin):
    """Stub derived class."""

    primitive: str = datafield(default="abc")
    """String key element."""

    embedded_1: StubDataclassRecordKey = datafield(default_factory=lambda: StubDataclassRecordKey("def"))
    """Embedded key 1."""

    embedded_2: StubDataclassRecordKey = datafield(default_factory=lambda: StubDataclassRecordKey("xyz"))
    """Embedded key 2."""

    def get_key_type(self) -> Type:
        return StubDataclassNestedFieldsKey

