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
from cl.runtime.storage.data_source_types import TKey
from cl.runtime.storage.data_source_types import TPack
from cl.runtime.storage.data_source_types import TQuery
from cl.runtime.storage.data_source_types import TRecord
from dataclasses import dataclass
from typing import ClassVar
from typing import Iterable


@dataclass(slots=True, init=True, frozen=True)
class DataSource(ABC):
    """Abstract base class for polymorphic data storage with dataset isolation."""

    __default: ClassVar[DataSource | None] = None

    data_source_id: str
    """Unique data source identifier."""

    @abstractmethod
    def batch_size(self) -> int:
        """Maximum number of records the data source will return in a single call, error if exceeded."""

    @abstractmethod
    def load_unordered(self, keys: Iterable[TKey], dataset: TDataset = None) -> Iterable[TRecord]:
        """
        Load records from the table associated with the base class of each key's type.

        Notes:
            The base type is determined using `key[0].get_base_type()`

        Returns:
            Iterable of TRecord = Tuple[TKey, TData, TIdentity, TDataset, TStamp]

        Args:
            keys: Iterable of TKey = (type, primary key fields)
            dataset: Lookup dataset as a list of path tokens (empty list or None means root dataset)
        """

    @abstractmethod
    def load_by_query(self, query: TQuery, dataset: TDataset = None) -> Iterable[TRecord]:
        """
        Load records based on the query.

        Returns:
            Iterable of TRecord = Tuple[TKey, TData, TIdentity, TDataset, TStamp]

        Args:
            query: Tuple of (TYPE, CONDITIONS_DICT, ORDER_DICT) where TYPE and its descendants will be
                returned by the query based on NoSQL query conditions and order in MongoDB format.
                Keys in CONDITIONS_DICT and ORDER_DICT must match the fields of TYPE.
            dataset: Lookup dataset as a list of path tokens (empty list or None means root dataset)
        """

    @abstractmethod
    def save_many(self, packs: Iterable[TPack], dataset: TDataset = None) -> None:
        """
        Save records to the table associated with the base class of each record's type.

        Notes:
            The base type is determined using `pack[0][0].get_base_type()`

        Args:
            packs: Iterable of (TKey, TData) where TKey is (type, primary key fields) and TData is serialized data
            dataset: Target dataset as a list of path tokens (empty list or None means root dataset)
        """

    @abstractmethod
    def delete_many(self, keys: Iterable[TKey], dataset: TDataset = None) -> None:
        """
        Delete records from the table associated with the base class of each record's type.

        Notes:
            The base type is determined using `key[0].get_base_type()`

        Args:
            keys: Iterable of TKey = (type, primary key fields)
            dataset: Target dataset as a list of path tokens (empty list or None means root dataset)
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
            data_source_type = ClassInfo.get_class_type(dynaconf_settings.data_source.type)
            DataSource.__default = data_source_type(dynaconf_settings.data_source)
        return DataSource.__default
