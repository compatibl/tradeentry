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
from dataclasses import dataclass
from typing import ClassVar
from typing import Iterable
from typing import Type
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.records.protocols import KeyProtocol, TQuery
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.settings.context_settings import ContextSettings
from cl.runtime.db.db_key import DataSourceKey
from cl.runtime.records.protocols import TKey
from cl.runtime.records.protocols import TRecord


@dataclass(slots=True, kw_only=True)
class DataSource(DataSourceKey, RecordMixin[DataSourceKey], ABC):
    """Polymorphic data storage with dataset isolation."""

    # TODO: Do not store here, instead get from settings once during the initial Context construction
    __default: ClassVar[DataSource | None] = None

    def get_key(self) -> DataSourceKey:
        return DataSourceKey(db_id=self.db_id)

    @abstractmethod
    def load_one(
        self,
        record_type: Type[TRecord],
        record_or_key: TRecord | KeyProtocol | tuple | str | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> TRecord | None:
        """
        Load a single record using a key (if a record is passed instead of a key, it is returned without DB lookup)

        Args:
            record_type: Record type to load, error if the result is not this type or its subclass
            record_or_key: Record (returned without lookup) or key in object, tuple or string format
            dataset: If specified, append to the root dataset of the database
            identity: Identity token for database access and row-level security
        """

    @abstractmethod
    def load_many(
        self,
        record_type: Type[TRecord],
        records_or_keys: Iterable[TRecord | KeyProtocol | tuple | str | None] | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[TRecord | None] | None:
        """
        Load records using a list of keys (if a record is passed instead of a key, it is returned without DB lookup),
        the result must have the same order as 'records_or_keys'.

        Args:
            record_type: Record type to load, error if the result is not this type or its subclass
            records_or_keys: Records (returned without lookup) or keys in object, tuple or string format
            dataset: If specified, append to the root dataset of the database
            identity: Identity token for database access and row-level security
        """

    @abstractmethod
    def load_all(
        self,
        record_type: Type[TRecord],
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[TRecord | None] | None:
        """
        Load all records of the specified type and its subtypes (excludes other types in the same DB table).

        Args:
            record_type: Record type to load, error if the result is not this type or its subclass
            dataset: If specified, append to the root dataset of the database
            identity: Identity token for database access and row-level security
        """

    @abstractmethod
    def load_filter(
        self,
        record_type: Type[TRecord],
        filter_obj: TRecord,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[TRecord]:
        """
        Load records where values of those fields that are set in the filter match the filter.

        Args:
            record_type: Record type to load, error if the result is not this type or its subclass
            filter_obj: Instance of 'record_type' whose fields are used for the query
            dataset: If specified, append to the root dataset of the database
            identity: Identity token for database access and row-level security
        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def delete_one(
        self,
        key_type: Type[TKey],
        key: TKey | KeyProtocol | tuple | str | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        """
        Delete one record for the specified key type using its key in one of several possible formats.

        Args:
            key_type: Key type to delete, used to determine the database table
            key: Key in object, tuple or string format
            dataset: If specified, append to the root dataset of the database
            identity: Identity token for database access and row-level security
        """

    @abstractmethod
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

    @abstractmethod
    def delete_all_and_drop_db(self) -> None:
        """
        IMPORTANT: !!! DESTRUCTIVE - THIS WILL PERMANENTLY DELETE ALL RECORDS WITHOUT THE POSSIBILITY OF RECOVERY

        Notes:
            This method will not run unless both db_id and database start with 'temp_db_prefix'
            specified using Dynaconf and stored in 'DataSourceSettings' class
        """

    @abstractmethod
    def close_connection(self) -> None:
        """Close database connection to releasing resource locks."""

    @classmethod
    def default(cls) -> DataSource:
        """Default database is initialized from settings and cannot be modified in code."""

        if DataSource.__default is None:
            # Load from configuration if not set
            context_settings = ContextSettings.instance()  # TODO: Refactor to place this inside Context
            db_type = ClassInfo.get_class_type(context_settings.db_class)
            # TODO: Add code to obtain from preloads if only key is specified
            DataSource.__default = db_type(db_id=context_settings.db_id)

        return DataSource.__default
