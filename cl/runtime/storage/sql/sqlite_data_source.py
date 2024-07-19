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
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from cl.runtime import DataSource
from cl.runtime.records.protocols import KeyProtocol, RecordProtocol
from cl.runtime.serialization.flat_dict_serializer import FlatDictSerializer
from cl.runtime.storage.data_source_types import TDataset, TIdentity, TQuery
from cl.runtime.storage.sql.sqlite_schema_manager import SqliteSchemaManager


@dataclass(slots=True, kw_only=True, frozen=True)
class SqliteDataSource(DataSource):

    db_name: str = 'test_db.sqlite'
    _connection: sqlite3.Connection = None
    _schema_manager: SqliteSchemaManager = None

    def __post_init__(self) -> None:
        """Initialize private attributes."""

        # TODO: Implement dispose logic
        # Use setattr to initialize attributes in a frozen object
        object.__setattr__(self, "_connection", sqlite3.connect(self.db_name))
        object.__setattr__(
            self, "_schema_manager", SqliteSchemaManager(sqlite_connection=self._connection)
        )

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

    def save_many(
            self, records: Iterable[RecordProtocol], *, dataset: TDataset = None, identity: TIdentity = None
    ) -> None:

        serializer = FlatDictSerializer()
        grouped_records = defaultdict(list)

        for record in records:
            grouped_records[record.get_key_type()].append(record)

        for key_type, records_group in grouped_records.items():

            serialized_records = [serializer.serialize_data(rec, is_root=True) for rec in records_group]
            all_fields = list({k for rec in serialized_records for k in rec.keys()})

            sql_values = tuple(
                serialized_record[k] if k in serialized_record else None
                for serialized_record in serialized_records
                for k in all_fields
            )

            columns_mapping = self._schema_manager.get_columns_mapping(key_type)
            quoted_columns = [f'"{columns_mapping[field]}"' for field in all_fields]
            columns_str = ", ".join(quoted_columns)

            values_str = ", ".join([f"({', '.join(['?']*len(all_fields))})" for _ in range(len(records_group))])

            table_name = self._schema_manager.table_name_for_type(key_type)

            self._schema_manager.create_table(table_name, columns_mapping.values(), if_not_exists=True)

            sql_statement = f"REPLACE INTO \"{table_name}\" ({columns_str}) VALUES {values_str};"

            cursor = self._connection.cursor()
            cursor.execute(sql_statement, sql_values)
            self._connection.commit()

    def delete_many(self, keys: Iterable[KeyProtocol] | None, *, dataset: TDataset = None,
                    identities: Iterable[TIdentity] | None = None) -> None:
        pass

    def delete_db(self) -> None:
        pass
