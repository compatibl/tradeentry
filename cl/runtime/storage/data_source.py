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

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.settings.runtime_settings import RuntimeSettings
from cl.runtime.storage.data_source_types import TDataset
from cl.runtime.storage.data_source_types import TIdentity
from cl.runtime.storage.data_source_types import TQuery
from dataclasses import dataclass
from typing import ClassVar
from typing import Iterable


@dataclass(slots=True, kw_only=True, frozen=True)
class DataSource(ABC):
    """Abstract base class for polymorphic data storage with dataset isolation."""

    # TODO: Do not store here, instead get from settings once during the initial Context construction
    __default: ClassVar[DataSource | None] = None

    data_source_id: str
    """Unique data source identifier."""

    @abstractmethod
    def load_one(
        self,
        record_or_key: KeyProtocol | None,
        *,
        dataset: TDataset = None,
        identity: TIdentity | None = None,
    ) -> RecordProtocol | None:
        """
        Load a single record using a key. If record is passed instead of a key, it is returned without DB lookup.

        Args:
            record_or_key: Record or key (records are returned without DB lookup)
            dataset: Lookup dataset as a delimited string, list of levels, or None
            identity: Identity token for row level access
        """

    @abstractmethod
    def load_many(
        self,
        records_or_keys: Iterable[KeyProtocol | None] | None,
        *,
        dataset: TDataset = None,
        identity: TIdentity | None = None,
    ) -> Iterable[RecordProtocol | None] | None:
        """
        Load records using a list of records or keys (records are returned without DB lookup).

        Args:
            records_or_keys: Iterable of records or keys (records are returned without DB lookup).
            dataset: Lookup dataset as a delimited string, list of levels, or None
            identity: Identity token for row level access
        """

    @abstractmethod
    def load_by_query(
        self,
        query: TQuery,
        *,
        dataset: TDataset = None,
        identity: TIdentity | None = None,
    ) -> Iterable[RecordProtocol]:
        """
        Load records based on the query.

        Args:
            query: Tuple of (TYPE, CONDITIONS_DICT, ORDER_DICT) where TYPE and its descendants will be
                returned by the query based on NoSQL query conditions and order in MongoDB format.
                Keys in CONDITIONS_DICT and ORDER_DICT must match the fields of TYPE.
            dataset: Lookup dataset as a delimited string, list of levels, or None
            identity: Identity token for row level access
        """

    @abstractmethod
    def save_one(
        self,
        record: RecordProtocol | None,
        *,
        dataset: TDataset = None,
        identity: TIdentity = None,
    ) -> None:
        """
        Save records to storage.

        Args:
            record: Record or None.
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token for row level access
        """

    @abstractmethod
    def save_many(
        self,
        records: Iterable[RecordProtocol],
        *,
        dataset: TDataset = None,
        identity: TIdentity = None,
    ) -> None:
        """
        Save records to storage.

        Args:
            records: Iterable of records.
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token for row level access
        """

    @abstractmethod
    def delete_many(
        self,
        keys: Iterable[KeyProtocol] | None,
        *,
        dataset: TDataset = None,
        identity: TIdentity | None = None,
    ) -> None:
        """
        Delete records using an iterable of keys.

        Args:
            keys: Iterable of keys.
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token for row level access
        """

    @abstractmethod
    def delete_db(self) -> None:
        """
        Permanently delete (drop) the database without the possibility of recovery.
        Error if data source identifier does not match the temp_db pattern in settings.
        """

    @staticmethod
    def default() -> DataSource:
        """Default data source is initialized from settings and cannot be modified in code."""

        if DataSource.__default is None:
            # Load from configuration if not set
            runtime_settings = RuntimeSettings.instance()
            data_source_type = ClassInfo.get_class_type(runtime_settings.data_source_class)
            data_source_id = str(runtime_settings.data_source_id)
            DataSource.__default = data_source_type(data_source_id=data_source_id)
        return DataSource.__default
