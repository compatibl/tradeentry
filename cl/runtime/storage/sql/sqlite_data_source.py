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
from typing import Iterable

from cl.runtime import DataSource
from cl.runtime.records.protocols import KeyProtocol, RecordProtocol
from cl.runtime.storage.data_source_types import TDataset, TIdentity, TQuery


class SqliteDataSource(DataSource):
    def batch_size(self) -> int:
        pass

    def load_one(self, record_or_key: KeyProtocol | None, *, dataset: TDataset = None,
                 identities: Iterable[TIdentity] | None = None) -> RecordProtocol | None:
        pass

    def load_many(self, records_or_keys: Iterable[KeyProtocol | None] | None, *, dataset: TDataset = None,
                  identities: Iterable[TIdentity] | None = None) -> Iterable[RecordProtocol | None] | None:

        pass

    def load_by_query(self, query: TQuery, *, dataset: TDataset = None,
                      identities: Iterable[TIdentity] | None = None) -> Iterable[RecordProtocol]:
        pass

    def save_one(self, record: RecordProtocol | None, *, dataset: TDataset = None, identity: TIdentity = None) -> None:
        # it is good to implement as save_many([record])
        pass

    def save_many(self, records: Iterable[RecordProtocol], *, dataset: TDataset = None,
                  identity: TIdentity = None) -> None:
        # records can be of different types. first step is to group them by type
        # inheritance: single table, or joined table
        # serialization format: how to serialize nested data objects / vectors?
        # should we use ORM? performance will be better with row-sql approach

        pass

    def delete_many(self, keys: Iterable[KeyProtocol] | None, *, dataset: TDataset = None,
                    identities: Iterable[TIdentity] | None = None) -> None:
        pass

    def delete_db(self) -> None:
        pass