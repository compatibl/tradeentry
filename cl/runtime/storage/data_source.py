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
from cl.runtime.classes.attrs import data_class
from cl.runtime.storage.data_source_key import DataSourceKey
from cl.runtime.classes.record_mixin import RecordMixin
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List


@data_class
class DataSource(DataSourceKey, RecordMixin, ABC):
    """Abstract base class for polymorphic data storage with dataset isolation."""

    @abstractmethod
    def load_many(
        self,
        table: str,
        keys: Iterable[Dict[str, Any] | str | None],
        dataset: List[str] | str | None = None,
    ) -> Iterable[Dict[str, Any] | None]:
        """
        Load serialized records from a single table using a list of keys.
        
        Returns:
            Iterable with the same length and in the same order as the list of keys containing dicts.
            where each level is a supported primitive type, list, or another dict.
            A result element is None if the record is not found or the key is None.

        Args:
            table: Table from which the records will be loaded.
            keys: Each element is either a dictionary of primary key fields or semicolon-delimited string.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def load_by_query(
        self,
        table: str,
        query: Dict[str, Any] | None,
        order: Dict[str, int] | None = None,
        dataset: List[str] | str | None = None,
    ) -> Iterable[Dict[str, Any]]:
        """
        Load serialized records from a single table by query.
        
        Returns:
            Iterable containing dicts where each level is a supported primitive type, list, or another dict.

        Args:
            table: Table from which the records will be loaded.
            query: NoSQL query as dict in MongoDB format, or None to load all records from the table.
            order: NoSQL sorting order in MongoDB format, or None if the result can be in any order.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def save_many(
        self,
        table: str,
        records: Iterable[Dict[str, Any] | None],
        dataset: List[str] | str | None = None,
    ) -> None:
        """
        Save serialized records to a single table (overwrite records that already exist).

        Args:
            table: Table to which the records will be saved.
            records: Iterable of dicts where each level is a supported primitive type, list, or another dict.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def delete_many(
        self,
        table: str,
        keys: Iterable[Dict[str, Any] | str],
        dataset: List[str] | str | None = None,
    ) -> None:
        """
        Delete records in the specified table using a list of keys (no error if does not exist).

        Args:
            table: Table from which the records will be deleted.
            keys: Each key is either a dictionary of primary key fields or semicolon-delimited string.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
        """

    @abstractmethod
    def delete_db(self) -> None:
        """
        Permanently delete (drop) the database without the possibility of recovery.
        Error if data source identifier does not match the temp_db pattern in settings.
        """
