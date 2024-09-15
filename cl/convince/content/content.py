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

from cl.runtime.records.record_mixin import RecordMixin
from cl.convince.content.content_key import ContentKey


@dataclass(slots=True, kw_only=True)
class Content(ContentKey, RecordMixin[ContentKey], ABC):
    """Content consumed or generated during AI workflows (derived classes provide format-specific functionality)."""

    @abstractmethod
    def as_str(self) -> str:
        """Convert to string format."""

    @classmethod
    @abstractmethod
    def from_str(cls, value: str) -> Self:
        """Convert from string format."""

    def get_key(self) -> ContentKey:
        return ContentKey(content_id=self.content_id)
