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
from typing import List

from cl.runtime import View
from cl.runtime.records.dataclasses_extensions import missing


@dataclass(slots=True, kw_only=True)
class KeyListView(View):
    """List of generic keys in ClassName;key_field_1;key_field_2 format, records are loaded and displayed."""

    key_list: List[str] = missing()
    """List of generic keys in ClassName;key_field_1;key_field_2 format, records are loaded and displayed."""
