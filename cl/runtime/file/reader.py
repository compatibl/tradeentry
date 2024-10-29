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
from cl.runtime.file.reader_key import ReaderKey
from cl.runtime.records.record_mixin import RecordMixin


@dataclass(slots=True, kw_only=True)
class Reader(ReaderKey, RecordMixin[ReaderKey], ABC):
    """Read records from the specified files or directories and save them to the current context."""

    def get_key(self) -> ReaderKey:
        return ReaderKey(loader_id=self.loader_id)

    @abstractmethod
    def read_and_save(self) -> None:
        """Read records from the specified files or directories and save them to the current context."""
