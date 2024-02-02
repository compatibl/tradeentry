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

from cl.runtime.storage.key import Key
from cl.runtime.storage.attrs_key_util import attrs_key
from cl.runtime.storage.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_record_key import StubAttrsRecordKey


@attrs_key
class StubAttrsNestedFieldsKey(Key):
    """Record where the key is composite and includes other keys."""

    primitive: str = attrs_field(default="abc")
    """String key element."""

    embedded_1: StubAttrsRecordKey = attrs_field(factory=StubAttrsRecordKey)
    """Embedded key 1."""

    embedded_2: StubAttrsRecordKey = attrs_field(factory=StubAttrsRecordKey)
    """Embedded key 2."""
