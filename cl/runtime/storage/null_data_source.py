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
from cl.runtime.storage.data_source_types import TQuery, TPack, TDataset
from cl.runtime.storage.data_source import TKey
from cl.runtime.storage.data_source import TRecord
from dataclasses import dataclass
from typing import Iterable
from typing import List
from typing import Tuple


@dataclass(slots=True, init=True, frozen=True)
class NullDataSource(DataSource):
    """Null data source discards the data written into it, and returns no data."""

    def batch_size(self) -> int:
        raise NotImplementedError()

    def load_unordered(
        self,
        keys: Iterable[TKey],
        dataset: TDataset = None,
    ) -> Iterable[TRecord]:
        raise NotImplementedError()

    def load_by_query(
        self,
        query: TQuery,
        dataset: TDataset = None,
    ) -> Iterable[TRecord]:
        raise NotImplementedError()

    def save_many(
        self,
        records: Iterable[TPack],
        dataset: TDataset = None,
    ) -> None:
        raise NotImplementedError()

    def delete_many(
        self,
        keys: Iterable[Tuple],
        dataset: TDataset = None,
    ) -> None:
        raise NotImplementedError()

    def delete_db(self) -> None:
        raise NotImplementedError()
