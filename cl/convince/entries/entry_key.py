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
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin
from cl.runtime.records.protocols import is_record


@dataclass(slots=True, kw_only=True)
class EntryKey(KeyMixin):
    """Performs comprehension of the specified entry text."""

    entry_type: str = missing()
    """Type string of the entry class in ClassName format."""

    entry_text: str = missing()
    """Full text of the entry."""

    def __post_init__(self):
        """Populate entry type if not set when called inside a record derived from key, leave blank if this is a key."""

        if self.entry_type is None and is_record(self):
            self.entry_type = type(self).__name__

    @classmethod
    def get_key_type(cls) -> Type:
        return EntryKey
