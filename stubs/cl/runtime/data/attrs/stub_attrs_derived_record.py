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
from cl.runtime.storage.index_util import index_fields
from cl.runtime.storage.attrs_record_util import attrs_record
from cl.runtime.storage.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_record import StubAttrsRecord


@index_fields('derived_field, -version')
@attrs_record(init=False)
class StubAttrsDerivedRecord(StubAttrsRecord):
    """Stub derived class."""

    derived_field: str = attrs_field(default="derived")
    """Stub field."""

    def non_virtual_derived_handler(self) -> None:
        pass

    def virtual_base_handler(self) -> None:
        pass

