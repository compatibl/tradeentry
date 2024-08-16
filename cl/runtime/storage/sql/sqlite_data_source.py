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
from cl.runtime import DataSource
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.records.protocols import is_key
from cl.runtime.serialization.flat_dict_serializer import FlatDictSerializer
from cl.runtime.storage.data_source_types import TDataset
from cl.runtime.storage.data_source_types import TIdentity
from cl.runtime.storage.data_source_types import TQuery
from cl.runtime.storage.sql.sqlite_schema_manager import SqliteSchemaManager
from collections import defaultdict
from dataclasses import dataclass
from itertools import groupby
from typing import Iterable, List, Tuple, Any, Dict
from typing import Type


def dict_factory(cursor, row):
    """sqlite3 row factory to return result as dictionary."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


@dataclass(slots=True, kw_only=True, frozen=True)
class SqliteDataSource(DataSource):
    """Sqlite data source without dataset and mile wide table for inheritance."""

    db_name: str = ":memory:"
    """Db name used to open sqlite connection."""

    _connection: sqlite3.Connection = None
    """Sqlite connection."""

    _schema_manager: SqliteSchemaManager = None
    """Sqlite schema manager."""

    def __post_init__(self) -> None:
        """Initialize private attributes."""

        # TODO: Implement dispose logic
        # Use setattr to initialize attributes in a frozen object
        object.__setattr__(self, "_connection", sqlite3.connect(self.db_name))
        self._connection.row_factory = dict_factory
        object.__setattr__(self, "_schema_manager", SqliteSchemaManager(sqlite_connection=self._connection))

    def batch_size(self) -> int:
        pass

    @staticmethod
    def _add_where_keys_in_clause(
        sql_statement: str,
        key_fields: Tuple[str, ...],
        columns_mapping: Dict[str, str],
        keys_len: int,
    ) -> str:
        """
        Add "WHERE (key_field1, ...) IN ((value1_for_field1, ...), (value2_for_field1, ...), ...)" clause to
        sql_statement.
        """

        # if key fields isn't empty add WHERE clause
        if key_fields:
            value_places = ", ".join([f'({", ".join(["?"] * len(key_fields))})' for _ in range(keys_len)])
            key_column_str = ", ".join([f'"{columns_mapping[key]}"' for key in key_fields])

            # add WHERE clause to sql_statement
            sql_statement += f" WHERE ({key_column_str}) IN ({value_places})"

        return sql_statement

    @staticmethod
    def _serialize_keys_to_flat_tuple(
        keys: Iterable[KeyProtocol], key_fields: Tuple[str, ...], serializer
    ) -> Tuple[Any, ...]:
        """
        Sequentially serialize key fields for each key in keys into a flat tuple of values.
        Expected all keys are of the same type for which key fields are specified.
        """

        return tuple(
            serializer.serialize_data(getattr(key, key_field)) for key in keys for key_field in key_fields
        )

    def load_one(
        self, record_or_key: KeyProtocol | None, *, dataset: TDataset = None, identity: TIdentity | None = None
    ) -> RecordProtocol | None:
        return next(iter(self.load_many([record_or_key], dataset=dataset, identity=identity)))

    # TODO (Roman): maybe return mapping {key: record} in load_many
    def load_many(
        self,
        records_or_keys: Iterable[KeyProtocol | None] | None,
        *,
        dataset: TDataset = None,
        identity: TIdentity | None = None,
    ) -> Iterable[RecordProtocol | None] | None:
        serializer = FlatDictSerializer()

        # it is important to preserve the original order of records_or_keys.
        # itertools.groupby works just like that and does not violate the order.

        # group by key type and then by it is key or record. if not keys - return themselves.
        for key_type, records_or_keys_group in groupby(records_or_keys, lambda x: x.get_key_type() if x else None):
            # handle None records_or_keys
            if key_type is None:
                yield from records_or_keys_group
                continue

            for is_key_group, keys_group in groupby(records_or_keys_group, lambda x: is_key(x)):
                # return directly if input is record
                if not is_key_group:
                    yield from keys_group
                    continue

                table_name = self._schema_manager.table_name_for_type(key_type)

                # if keys_group don't support "in" or "len" operator convert it to tuple
                if not hasattr(keys_group, "__contains__") or not hasattr(keys_group, "__len__"):
                    keys_group = tuple(keys_group)

                # return None for all keys in group if table doesn't exist
                existing_tables = self._schema_manager.existing_tables()
                if table_name not in existing_tables:
                    yield from (None for _ in range(len(keys_group)))
                    continue

                key_fields = self._schema_manager.get_primary_keys(key_type)
                columns_mapping = self._schema_manager.get_columns_mapping(key_type)

                # if keys_group don't support "in" or "len" operator convert it to tuple
                sql_statement = f'SELECT * FROM "{table_name}"'
                sql_statement = self._add_where_keys_in_clause(
                    sql_statement, key_fields, columns_mapping, len(keys_group)
                )
                sql_statement += ";"

                # serialize keys to tuple
                query_values = self._serialize_keys_to_flat_tuple(keys_group, key_fields, serializer)

                cursor = self._connection.cursor()
                cursor.execute(sql_statement, query_values)

                reversed_columns_mapping = {v: k for k, v in columns_mapping.items()}

                # TODO (Roman): investigate performance impact from this ordering approach
                # bulk load from db returns records in any order so we need to check all records in group before return
                # collect db result to dictionary to return it according to input keys order
                result = {}
                for data in cursor.fetchall():
                    # TODO (Roman): select only needed columns on db side.
                    data = {reversed_columns_mapping[k]: v for k, v in data.items() if v is not None}
                    deserialized_data = serializer.deserialize_data(data)

                    # TODO (Roman): make key hashable and remove conversion of key to str
                    result[str(deserialized_data.get_key())] = deserialized_data

                # yield records according to input keys order
                for key in keys_group:
                    yield result.get(str(key))

    def load_by_query(
        self, query: TQuery, *, dataset: TDataset = None, identities: Iterable[TIdentity] | None = None
    ) -> Iterable[RecordProtocol]:
        raise NotImplementedError

    def load_all(self, record_type: Type[RecordProtocol]) -> Iterable[RecordProtocol]:
        """Load all records for given type including derived."""
        serializer = FlatDictSerializer()

        table_name: str = self._schema_manager.table_name_for_type(record_type)

        # if table doesn't exist return empty list
        if table_name not in self._schema_manager.existing_tables():
            return list()

        # get subtypes for record_type and use them in match condition
        subtype_names = tuple(self._schema_manager.get_subtype_names(record_type))
        value_placeholders = ", ".join(["?"] * len(subtype_names))
        sql_statement = f'SELECT * FROM "{table_name}" WHERE _type in ({value_placeholders});'

        reversed_columns_mapping = {
            v: k for k, v in self._schema_manager.get_columns_mapping(record_type.get_key_type(None)).items()
        }

        cursor = self._connection.cursor()
        cursor.execute(sql_statement, subtype_names)

        for data in cursor.fetchall():
            # TODO (Roman): select only needed columns on db side.
            data = {reversed_columns_mapping[k]: v for k, v in data.items() if v is not None}
            yield serializer.deserialize_data(data)

    def save_one(self, record: RecordProtocol | None, *, dataset: TDataset = None, identity: TIdentity = None) -> None:
        return self.save_many([record], dataset=dataset, identity=identity)

    def save_many(
        self, records: Iterable[RecordProtocol], *, dataset: TDataset = None, identity: TIdentity = None
    ) -> None:
        serializer = FlatDictSerializer()

        grouped_records = defaultdict(list)

        # TODO (Roman): improve grouping
        for record in records:
            grouped_records[record.get_key_type()].append(record)

        for key_type, records_group in grouped_records.items():

            # serialize records
            serialized_records = [serializer.serialize_data(rec, is_root=True) for rec in records_group]

            # get maximum set of fields from records
            all_fields = list({k for rec in serialized_records for k in rec.keys()})

            # fill sql_values with ordered values from serialized records
            # if field isn't in some records - fill with None
            sql_values = tuple(
                serialized_record[k] if k in serialized_record else None
                for serialized_record in serialized_records
                for k in all_fields
            )

            columns_mapping = self._schema_manager.get_columns_mapping(key_type)
            quoted_columns = [f'"{columns_mapping[field]}"' for field in all_fields]
            columns_str = ", ".join(quoted_columns)

            value_placeholders = ", ".join([f"({', '.join(['?']*len(all_fields))})" for _ in range(len(records_group))])

            table_name = self._schema_manager.table_name_for_type(key_type)

            primary_keys = [
                columns_mapping[primary_key] for primary_key in self._schema_manager.get_primary_keys(key_type)
            ]

            self._schema_manager.create_table(
                table_name, columns_mapping.values(), if_not_exists=True, primary_keys=primary_keys
            )

            sql_statement = f'REPLACE INTO "{table_name}" ({columns_str}) VALUES {value_placeholders};'

            if not primary_keys:
                # TODO (Roman): this is a workaround for handling singleton records.
                #  Since they don't have primary keys, we can't automatically replace existing records.
                #  So this code just deletes the existing records before saving.
                #  As a possible solution, we can introduce some mandatory primary key that isn't based on the
                #  key fields.
                self.delete_many((rec.get_key() for rec in records_group))

            cursor = self._connection.cursor()
            cursor.execute(sql_statement, sql_values)

            self._connection.commit()

    def delete_many(
        self,
        keys: Iterable[KeyProtocol] | None,
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> None:
        serializer = FlatDictSerializer()

        grouped_keys = defaultdict(list)

        # TODO (Roman): improve grouping
        for key in keys:
            grouped_keys[key.get_key_type()].append(key)

        for key_type, keys_group in grouped_keys.items():
            table_name = self._schema_manager.table_name_for_type(key_type)

            existing_tables = self._schema_manager.existing_tables()
            if table_name not in existing_tables:
                continue

            key_fields = self._schema_manager.get_primary_keys(key_type)
            columns_mapping = self._schema_manager.get_columns_mapping(key_type)

            # if keys_group don't support "in" or "len" operator convert it to tuple
            if not hasattr(keys_group, "__contains__") or not hasattr(keys_group, "__len__"):
                keys_group = tuple(keys_group)

            # construct sql_statement with placeholders for values
            sql_statement = f'DELETE FROM "{table_name}"'
            sql_statement = self._add_where_keys_in_clause(sql_statement, key_fields, columns_mapping, len(keys_group))
            sql_statement += ";"

            # serialize keys to tuple
            query_values = self._serialize_keys_to_flat_tuple(keys_group, key_fields, serializer)

            # perform delete query
            cursor = self._connection.cursor()
            cursor.execute(sql_statement, query_values)
            self._connection.commit()

    def delete_db(self) -> None:
        """Delete all tables and indexes on current db instance."""

        # delete several time because tables depended on foreign key can not be deleted before related tables exist.
        while True:
            if not self._connection:
                break

            cursor = self._connection.cursor()

            # delete tables
            delete_all_tables = [
                str(next(iter(x.values())))
                for x in cursor.execute(
                    "select 'drop table ' || name || ';' from sqlite_master where type = 'table';",
                ).fetchall()
            ]

            for delete_statement in delete_all_tables:
                cursor.execute(delete_statement)

            # delete indexes
            delete_all_indexes = [
                str(next(iter(x.values())))
                for x in cursor.execute(
                    "select 'drop index ' || name || ';' from sqlite_master where type = 'index';",
                ).fetchall()
            ]

            for delete_statement in delete_all_indexes:
                cursor.execute(delete_statement)

            # stop if nothing to delete
            if len(delete_all_tables) == 0 and len(delete_all_indexes) == 0:
                break

        # close connection
        if self._connection:
            self._connection.close()

        # TODO (Roman): delete db file
