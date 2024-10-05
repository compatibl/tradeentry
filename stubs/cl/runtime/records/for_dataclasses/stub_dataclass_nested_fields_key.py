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
from typing import Type
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_record import StubDataclassRecordKey


@dataclass(slots=True, kw_only=True)
class StubDataclassNestedFieldsKey(KeyMixin):
    """Stub derived class."""

    primitive: str = "abc"
    """String key element."""

    # TODO(CaseUtil): Convert to embedded1 when roundtrip serialization with digits is supported
    embedded1: StubDataclassRecordKey = field(default_factory=lambda: StubDataclassRecordKey(id="def"))
    """Embedded key 1."""

    # TODO(CaseUtil): Convert to embedded1 when roundtrip serialization with digits is supported
    embedded2: StubDataclassRecordKey = field(default_factory=lambda: StubDataclassRecordKey(id="xyz"))
    """Embedded key 2."""

    @classmethod
    def get_key_type(cls) -> Type:
        return StubDataclassNestedFieldsKey
