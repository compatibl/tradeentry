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

from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.data.key import Key


@attrs_record
class StubAttrsCircularReferenceKey(Key):
    """This stub record includes self as its element."""

    record_id: str = attrs_field()
    """Unique identifier."""
