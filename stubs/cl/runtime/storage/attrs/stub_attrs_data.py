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

from typing import Optional
from cl.runtime.storage.data import Data
from cl.runtime.storage.attrs_data_util import attrs_data
from cl.runtime.storage.attrs import attrs_field, attrs_class


@attrs_data
class StubAttrsData(Data):
    """Stub base data type."""

    str_field: str = attrs_field(default="abc")
    """Stub field."""

    int_field: int = attrs_field(default=123)
    """Stub field."""
