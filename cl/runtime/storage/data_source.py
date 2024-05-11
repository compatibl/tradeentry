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
from cl.runtime.storage.data_source_types import GenericKey, GenericPack, GenericDataset
from cl.runtime.storage.data_source_types import GenericQuery
from cl.runtime.storage.data_source_types import GenericRecord
from cl.runtime.settings.config import dynaconf_settings
from dataclasses import dataclass
from typing import ClassVar
from typing import Iterable
from typing import List


@dataclass(slots=True, init=True, frozen=True)
class DataSource(ABC):
    """Abstract base class for polymorphic data storage with dataset isolation."""

    __default: ClassVar[DataSource | None] = None

    data_source_id: str
    """Unique data source identifier."""

    @abstractmethod
    def batch_size(self) -> int:
        """Maximum number or records the data source will return in a single call, error if exceeded."""

    @abstractmethod
    def load_unordered(
        self,
        keys: Iterable[GenericKey],
        dataset: GenericDataset = None,
    ) -> Iterable[GenericRecord]:
        """
        Load records from the table associated with the base class of each key's type.

        Notes:
            The base type is determined using `key[0].get_base_type()`. Override if required.

        Returns:
            Tuples of (KEY, DATA, IDENTITY, DATASET, TIMESTAMP) where:
                - KEY: A tuple of (type,primary key fields)
                - DATA: Serialized record data in dictionary format (other formats may be added in the future)
                - IDENTITY: Identity data used for row level security
                - DATASET: Record's dataset as a list of path tokens (empty list or None means root dataset)
                - TIMESTAMP: Timestamp for the time the record was written to storage

        Args:
            keys: Tuple of the key type followed by the primary key fields in the order of declaration.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def load_by_query(
        self,
        query: GenericQuery,
        dataset: GenericDataset = None,
    ) -> Iterable[GenericRecord]:
        """
        Load records based on the query.

        Returns:
            Tuples of (KEY, DATA, IDENTITY, DATASET, TIMESTAMP) where:
                - KEY: A tuple of (type,primary key fields)
                - DATA: Serialized record data in dictionary format (other formats may be added in the future)
                - IDENTITY: Identity data used for row level security
                - DATASET: Record's dataset as a list of path tokens (empty list or None means root dataset)
                - TIMESTAMP: Timestamp for the time the record was written to storage

        Args:
            query: Tuple of (TYPE,CONDITIONS_DICT,ORDER_DICT) where TYPE and its descendants will be
                returned by the query based on NoSQL query conditions and order in MongoDB format.
                Keys in CONDITIONS_DICT and ORDER_DICT must match the fields of TYPE.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def save_many(
        self,
        records: Iterable[GenericPack],
        dataset: GenericDataset = None,
    ) -> None:
        """
        Save records to the table associated with the base class of each record's type. Overwrites existing records.

        Notes:
            The base type is determined using `record_type.get_base_type()`. Override if required.

        Args:
            records: Tuples of (KEY, DATA) where KEY=(type, primary key fields) and DATA is serialized record data.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def delete_many(
        self,
        keys: Iterable[GenericKey],
        dataset: GenericDataset = None,
    ) -> None:
        """
        Delete records from the table associated with each key's base type.

        Notes:
            The base type is determined using `key[0].get_base_type()`

        Args:
            keys: Tuple of the key type followed by the primary key fields in the order of declaration.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
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
