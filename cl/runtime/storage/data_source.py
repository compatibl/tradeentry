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
from cl.runtime.settings.config import dynaconf_settings
from cl.runtime.storage.data_source_types import TDataset
from cl.runtime.storage.data_source_types import TIdentity
from cl.runtime.storage.data_source_types import TKey
from cl.runtime.storage.data_source_types import TLoadedRecord
from cl.runtime.storage.data_source_types import TPackedRecord
from cl.runtime.storage.data_source_types import TQuery
from dataclasses import dataclass
from typing import ClassVar
from typing import Iterable
from typing import List


@dataclass(slots=True, kw_only=True, frozen=True)
class DataSource(ABC):
    """Abstract base class for polymorphic data storage with dataset isolation."""

    __default: ClassVar[DataSource | None] = None

    data_source_id: str
    """Unique data source identifier."""

    @abstractmethod
    def batch_size(self) -> int:
        """Maximum number of records the data source will return in a single call, error if exceeded."""

    @abstractmethod
    def load_many(
        self,
        keys: Iterable[TKey],
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> Iterable[TLoadedRecord]:
        """
        Load records using a list of keys where each key specifies the table and primary key fields.

        Returns:
            Iterable of TLoadedRecord = Tuple[TKey, TData, TIdentity, TDataset, TStamp]

        Args:
            keys: Iterable of keys in (table_type, primary_key_1, primary_key_2, ...) format
            dataset: Lookup dataset as a delimited string, list of levels, or None
            identities: Only the records whose identity matches one of the argument identities will be loaded
        """

    @abstractmethod
    def load_by_query(
        self,
        query: TQuery,
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> Iterable[TLoadedRecord]:
        """
        Load records based on the query.

        Returns:
            Iterable of TLoadedRecord = Tuple[TKey, TData, TIdentity, TDataset, TStamp]

        Args:
            query: Tuple of (TYPE, CONDITIONS_DICT, ORDER_DICT) where TYPE and its descendants will be
                returned by the query based on NoSQL query conditions and order in MongoDB format.
                Keys in CONDITIONS_DICT and ORDER_DICT must match the fields of TYPE.
            dataset: Lookup dataset as a delimited string, list of levels, or None
            identities: Only the records whose identity matches one of the argument identities will be loaded
        """

    @abstractmethod
    def save_many(
        self, packs: Iterable[TPackedRecord], *, dataset: TDataset = None, identity: TIdentity = None
    ) -> None:
        """
        Save records in (TKey, TData) format where
            - TKey is (table_type, primary_key_1, primary_key_2, ...)
            - TData is serialized data

        Args:
            packs: Iterable of (TKey, TData)
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token used for row level security
        """

    @abstractmethod
    def delete_many(
        self,
        keys: Iterable[TKey],
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> None:
        """
        Delete records using a list of keys where each key specifies the table and primary key fields.

        Args:
            keys: Iterable of keys in (table_type, primary_key_1, primary_key_2, ...) format
            dataset: Target dataset as a delimited string, list of levels, or None
            identities: Only the records whose identity matches one of the argument identities will be deleted
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
            data_source_type = ClassInfo.get_class_type(dynaconf_settings["context"]["data_source"].pop("_class"))
            DataSource.__default = data_source_type(**dynaconf_settings["context"]["data_source"])
        return DataSource.__default
