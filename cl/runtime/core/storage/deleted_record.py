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
from typing import Any, Dict, Optional

from cl.runtime.core.storage.class_field import class_field
from cl.runtime.core.storage.record import Record


@dataclass
class DeletedRecord(Record):
    """
    Represents a deleted record in commit queue and in those
    cases when the database is write-once, or to shadow records
    in parent datasets or data sources from lookup.
    """

    pk: str = class_field()
    """Primary key (PK) string."""

    def get_pk(self) -> str:
        """Return primary key (PK) as string."""
        return self.pk

    def to_dict(self) -> Dict[str, Any]:
        """Serialize self as dictionary (may return shallow copy)."""
        raise RuntimeError('Attempting to serialize a deleted record.')

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Populate self from dictionary (must perform deep copy)."""
        raise RuntimeError('Attempting to deserialize a deleted record.')
