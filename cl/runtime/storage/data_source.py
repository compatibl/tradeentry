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
from cl.runtime.storage.attrs import data_class
from cl.runtime.storage.data_source_key import DataSourceKey
from cl.runtime.storage.record_mixin import RecordMixin
from typing import Dict, Any, Iterable, List


@data_class
class DataSource(DataSourceKey, RecordMixin, ABC):
    """Abstract base class for polymorphic data storage with dataset isolation."""

    @abstractmethod
    def load_many(
        self,
        table: str,
        keys: Iterable[Dict[str, Any] | str],
        data_set: List[str] | str | None = None,
    ) -> Iterable[Dict[str, Any] | None]:
        """
        Load records serialized into dicts from the specified table using a list of keys.

        Args:
            table: Table from which the records will be deleted
            keys: Each key is either a dictionary of primary key fields or semicolon-delimited string
            data_set: List of datasets in lookup order, single dataset, or None for root dataset
        """

    @abstractmethod
    def load_by_query(
        self,
        table: str,
        query: Dict[str, Any],
        data_set: List[str] | str | None = None,
    ) -> Iterable[Dict[str, Any]]:
        """
        Load records serialized into dicts from the specified table using a query.

        Args:
            table: Table from which the records will be deleted
            query: Dictionary of conditions
            data_set: List of datasets in lookup order, single dataset, or None for root dataset
        """

    @abstractmethod
    def save_many(
            self,
            table: str,
            records: Iterable[Dict[str, Any]],
            data_set: List[str] | str | None = None,
    ) -> None:
        """
        Save records serialized as dicts into the specified table (overwrite if already exists).

        Args:
            table: Table to which the records will be saved
            records: Each serialized into dict where each level is primitive type, dict, or list.
            data_set: List of datasets in lookup order, single dataset, or None for root dataset
        """

    @abstractmethod
    def delete_many(
            self,
            table: str,
            keys: Iterable[Dict[str, Any] | str],
            data_set: List[str] | str | None = None,
    ) -> None:
        """
        Delete records in the specified table using a list of keys (no error if does not exist).

        Args:
            table: Table from which the records will be deleted
            keys: Each key is either a dictionary of primary key fields or semicolon-delimited string
            data_set: List of datasets in lookup order, single dataset, or None for root dataset
        """

    @abstractmethod
    def delete_db(self) -> None:
        """
        Permanently delete (drop) the database without the possibility of recovery.
        Error if data source identifier does not match the temp_db pattern in settings.
        """
