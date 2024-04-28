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

from cl.runtime import DataSource
from dataclasses import dataclass
from dataclasses import field
from typing import Any, TYPE_CHECKING
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Type
from cl.runtime.storage.data_source import PackType, KeyType


@dataclass(slots=True, init=True, frozen=True)
class NullDataSource(DataSource):
    """Null data source discards the data written into it, and returns no data."""

    def batch_size(self) -> int:
        raise NotImplementedError()

    def load_unordered(
        self,
        base_type: Type,
        keys: Iterable[KeyType],
        dataset: List[str] | str | None = None,
    ) -> Iterable[PackType]:
        
        raise NotImplementedError()

    def load_by_query(
        self,
        base_type: Type,
        match_type: Type,
        query: Dict[str, Any] | None,
        order: Dict[str, int] | None = None,
        dataset: List[str] | str | None = None,
    ) -> Iterable[PackType]:
        
        raise NotImplementedError()

    def save_many(
        self,
        base_type: Type,
        records: Iterable[PackType],
        dataset: List[str] | str | None = None,
    ) -> None:

        raise NotImplementedError()

    def delete_many(
        self,
        keys: Iterable[Tuple],
        dataset: List[str] | str | None = None,
    ) -> None:

        raise NotImplementedError()

    def delete_db(self) -> None:

        raise NotImplementedError()
