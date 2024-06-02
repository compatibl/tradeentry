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

from cl.runtime.records.dataclasses.dataclass_mixin import DataclassMixin
from dataclasses import dataclass
from dataclasses import field

from stubs.cl.runtime.records.dataclasses.stub_dataclass_base_key import StubDataclassBaseKey


@dataclass
class StubDataclassBase(DataclassMixin):
    """Stub record base class."""

    str_field: str = field(default="abc")
    """Stub field."""

    int_field: int = field(default=123)
    """Stub field."""

    def get_key(self) -> StubDataclassBaseKey:
        return type(self), self.str_field, self.int_field
