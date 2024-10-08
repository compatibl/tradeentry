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

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from typing_extensions import Self

from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.convince.entries.entry_key import EntryKey
from cl.convince.entries.entry_status_enum import EntryStatusEnum


@dataclass(slots=True, kw_only=True)
class Entry(EntryKey, RecordMixin[EntryKey], ABC):
    """Contains text and supporting data along with the results of their processing."""

    type_: str = missing()
    """Type in ClassName format without module (included in MD5 hash)."""

    title: str = missing()
    """Title of a long entry or complete description of a short one (included in MD5 hash)."""

    body: str | None = None
    """Optional body of the entry if not completely described by the title (included in MD5 hash)."""

    data: str | None = None
    """Optional supporting data in YAML format (included in MD5 hash)."""

    status: EntryStatusEnum = missing()
    """Processing status and if the entry was created by AI or code or by a human."""

    def get_key(self) -> EntryKey:
        return EntryKey(entry_id=self.entry_id)

    @classmethod
    @abstractmethod
    def create(
            cls,
            title: str,
            *,
            body: str | None = None,
            data: str | None = None,
    ) -> Self:
        """Create and save to storage using type and title with optional body and data parameters."""

    @classmethod
    def create_self(
            cls,
            title: str,
            *,
            body: str | None = None,
            data: str | None = None,
            status: EntryStatusEnum = EntryStatusEnum.COMPLETED,
    ) -> Self:
        """Create self from type and title with optional body, data and status parameters."""

        # Create key (includes generation of MD5 hash when body or data are empty)
        entry_key = cls.create_key(
            title=title,
            body=body,
            data=data,
        )

        # Type is ClassName without module
        type_ = cls.__name__

        # Create self and populate fields of the base class
        result = cls(
            entry_id=entry_key.entry_id,
            type_=type_,
            title=title,
            body=body,
            data=data,
            status=status,
        )

        return result
