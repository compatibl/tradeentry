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

from cl.runtime.backend.core.ui_type_state_key import UiTypeStateKey
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import final


@final
@dataclass(slots=True, kw_only=True)
class UiTypeState(UiTypeStateKey, RecordMixin[UiTypeStateKey]):
    """Defines ui settings for a type."""

    read_only: Optional[bool] = missing()
    """Specifies if records of this type are readonly."""

    use_cache: Optional[bool] = missing()
    """
    If set and TRUE data will be cached until tab is opened. This means that the next time the tab is
    activated, the main grid data request will not be submitted, it will be taken from the browser cache.
    """

    pinned_handlers: Optional[List[str]] = missing()
    """List of names of the handlers pinned for the type"""

    def get_key(self) -> UiTypeStateKey:
        return UiTypeStateKey(type_=self.type_, user=self.user)
