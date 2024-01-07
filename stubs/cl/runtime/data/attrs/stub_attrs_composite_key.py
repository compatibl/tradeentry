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

from cl.runtime.data.key import Key
from cl.runtime.data.attrs.attrs_key_util import attrs_key
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.data.attrs.stubs.stub_attrs_base_record_key import StubAttrsBaseRecordKey


@attrs_key
class StubAttrsCompositeKey(Key):
    """Record where the key is composite and includes other keys."""

    str_key_0: str = attrs_field()
    """String key element."""

    embedded_key_1: StubAttrsBaseRecordKey = attrs_field()
    """Embedded key 1."""

    embedded_key_2: StubAttrsBaseRecordKey = attrs_field()
    """Embedded key 2."""
