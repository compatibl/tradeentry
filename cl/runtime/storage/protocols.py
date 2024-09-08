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

from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.storage.data_source_types import TQuery
from typing import Iterable
from typing import Protocol
from typing import Type


class DataSourceProtocol(Protocol):
    """Protocol for a data source providing polymorphic data storage with dataset isolation."""

    def load_one(
        self,
        record_or_key: KeyProtocol | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> RecordProtocol | None:
        """
        Load a single record using a key. If record is passed instead of a key, it is returned without DB lookup.

        Args:
            record_or_key: Record or key (records are returned without DB lookup)
            dataset: If specified, append to the root dataset of the data source
            identity: Identity token for database access and row-level security
        """

    def load_many(
        self,
        records_or_keys: Iterable[KeyProtocol | None] | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[RecordProtocol | None] | None:
        """
        Load records using a list of records or keys (records are returned without DB lookup).

        Args:
            records_or_keys: Iterable of records or keys (records are returned without DB lookup).
            dataset: If specified, append to the root dataset of the data source
            identity: Identity token for database access and row-level security
        """

    def load_all(
        self,
        record_type: Type[RecordProtocol],
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[RecordProtocol]:
        """
        Load all records of the specified type.

        Args:
            record_type: Type of the record to load.
            dataset: If specified, append to the root dataset of the data source
            identity: Identity token for database access and row-level security
        """

    def load_by_query(
        self,
        query: TQuery,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[RecordProtocol]:
        """
        Load records based on the query.

        Args:
            query: Tuple of (TYPE, CONDITIONS_DICT, ORDER_DICT) where TYPE and its descendants will be
                returned by the query based on NoSQL query conditions and order in MongoDB format.
                Keys in CONDITIONS_DICT and ORDER_DICT must match the fields of TYPE.
            dataset: If specified, append to the root dataset of the data source
            identity: Identity token for database access and row-level security
        """

    def save_one(
        self,
        record: RecordProtocol | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        """
        Save records to storage.

        Args:
            record: Record or None.
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token for database access and row-level security
        """

    def save_many(
        self,
        records: Iterable[RecordProtocol],
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        """
        Save records to storage.

        Args:
            records: Iterable of records.
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token for database access and row-level security
        """

    def delete_many(
        self,
        keys: Iterable[KeyProtocol] | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        """
        Delete records using an iterable of keys.

        Args:
            keys: Iterable of keys.
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token for database access and row-level security
        """

    def delete_all(self) -> None:
        """
        Permanently delete (drop) the database without the possibility of recovery.
        Error if data source identifier does not match the temp_db pattern in settings.
        """
