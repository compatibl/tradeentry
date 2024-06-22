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

from cl.runtime.records.dataclasses.dataclass_record_mixin import datafield
from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class StubDataclassData:
    """Stub base data type."""

    str_field: str = datafield(default="abc")
    """Stub field."""

    int_field: int = datafield(default=123)
    """Stub field."""
