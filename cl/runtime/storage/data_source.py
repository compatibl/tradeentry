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
from cl.runtime.records.record_annotations import GenericKey, GenericQuery, GenericOrder
from cl.runtime.records.record_annotations import GenericRecord
from cl.runtime.settings.config import dynaconf_settings
from dataclasses import dataclass
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Iterable
from typing import List
from typing import Type


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
        base_type: Type,
        keys: Iterable[GenericKey],
        dataset: List[str] | str | None = None,
    ) -> Iterable[GenericRecord]:
        """
        Load serialized records from a single table associated with `base_type` using a list of keys.

        Returns:
            Tuples of (KEY,DICT) where KEY=(type,primary key fields) and DICT contains serialized record data.

        Args:
            base_type: Base type determines the table where data source operations are performed.
            keys: Tuple of primary key fields in the order of declaration.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def load_by_query(
        self,
        base_type: Type,
        match_type: Type,
        query: GenericQuery | None,
        order: GenericOrder | None = None,
        dataset: List[str] | str | None = None,
    ) -> Iterable[GenericRecord]:
        """
        Load serialized records from a single table associated with `base_type` by query.

        Returns:
            Tuples of (KEY,DICT) where KEY=(type,primary key fields) and DICT contains serialized record data.

        Args:
            base_type: Base type determines the table where data source operations are performed.
            match_type: Query will only match objects of this type and its descendants. Must derive from `base_type`.
            query: NoSQL query on fields of `match_type` class in MongoDB format, or None to load all records.
            order: NoSQL order defined on fields of `match_type` in MongoDB format, or None if no sorting is required.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def save_many(
        self,
        records: Iterable[GenericRecord],
        dataset: List[str] | str | None = None,
    ) -> None:
        """
        Save records to the table associated with the record's base type. Overwrites existing records.

        Notes:
            The base type is determined using class method `record_type.get_base_type()`

        Args:
            records: Tuples of (KEY,DICT) where KEY=(type,primary key fields) and DICT contains serialized record data.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def delete_many(
        self,
        base_type: Type,
        keys: Iterable[GenericKey],
        dataset: List[str] | str | None = None,
    ) -> None:
        """
        Delete records a single table associated with `base_type` using a list of keys (no error if does not exist).

        Args:
            base_type: Base type determines the table where data source operations are performed.
            keys: Tuple of primary key fields in the order of declaration.
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
