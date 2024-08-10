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
from cl.runtime.schema.schema import Schema
from dataclasses import dataclass
from dataclasses import field
from inflection import camelize
from memoization import cached
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple
from typing import Type


@dataclass(slots=True, kw_only=True)
class SqliteSchemaManager:
    """Class to manage the sqlite schema (table names, columns mapping etc.)."""

    sqlite_connection: sqlite3.Connection = None
    """Sqlite connection."""

    pascalize_column_names: bool = False
    """If True - convert column names to pascal case."""

    add_class_to_column_names: bool = True
    """If True - class name will be added to the column name in format ClassName.field_name."""

    def create_table(self, table_name: str, columns: Iterable[str], if_not_exists: bool = True) -> None:
        """
        Create sqlite table with given name and columns.

        No need to specify column types because sqlite supports dynamic typing.
        Mile wide table contains columns for all subtypes.
        """

        if_not_exists_part: str = " IF NOT EXISTS" if if_not_exists else ""
        columns_str: str = '"' + '", "'.join(columns) + '"'

        # construct final create table statement
        create_table_statement: str = f"CREATE TABLE{if_not_exists_part} {table_name} ({columns_str});"

        # execute create table statement
        cursor = self.sqlite_connection.cursor()
        cursor.execute(create_table_statement)

        create_unique_index_statement = f'CREATE UNIQUE INDEX IF NOT EXISTS idx_key ON "{table_name}" (_key);'
        cursor.execute(create_unique_index_statement)

        self.sqlite_connection.commit()

    def delete_table_by_name(self, name: str, if_exists: bool = True) -> None:
        """Delete table in db."""
        cursor = self.sqlite_connection.cursor()
        if_exists_part: str = " IF EXISTS" if if_exists else ""
        cursor.execute(f"DROP TABLE {if_exists_part} '{name}';")
        self.sqlite_connection.commit()

    def table_name_for_type(self, type_: Type) -> str:
        """Return table name for the given type."""
        key_type = self._get_key_type(type_)

        # return table name as key type name without 'Key' suffix
        return key_type.__name__.removesuffix("Key")

    def existing_tables(self) -> List[str]:
        """Return existing tables in db."""
        cursor = self.sqlite_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # cursor.fetchall() returns [{'name': name},]
        return [select_res["name"] for select_res in cursor.fetchall()]

    def _get_key_type(self, type_: Type) -> Type:
        """Get key type for the given type."""
        get_key_type = getattr(type_, "get_key_type", None)
        if get_key_type is None:
            raise RuntimeError(f"Type {type_} is not record type.")

        # get key attributes
        return get_key_type(None)

    def _get_type_fields(self, type_: Type) -> Dict[str, Type]:
        """Return field name and type of annotation based type declaration."""
        return type_.__annotations__

    # TODO (Roman): make cached but only for key types
    def get_columns_mapping(self, type_: Type) -> Dict[str, str]:
        """Collect all types in hierarchy and check type conflicts for fields with the same name."""

        types_in_hierarchy = Schema.get_types_in_hierarchy(type_)
        key_type = self._get_key_type(type_)

        # get key attributes
        key_fields_class_name: str = key_type.__name__.removesuffix("Key")
        key_fields = self._get_type_fields(key_type)

        # {field_name: (subclass_name, field_type)}
        all_fields: Dict[str, Tuple[str, Type]] = {
            key_field_name: (key_fields_class_name, key_field_type)
            for key_field_name, key_field_type in key_fields.items()
        }

        for type_ in types_in_hierarchy:
            fields = self._get_type_fields(type_).items()
            for field_name, field_type in fields:
                existing_field = all_fields.get(field_name)

                if existing_field is not None:
                    # check if fields with the same name have compatible type
                    if not issubclass(field_type, existing_field[1]):
                        raise TypeError(
                            f"Field {field_name}: {field_type} of class {type_.__name__} conflicts with the same field "
                            f"{field_name}: {existing_field[1]} in base class {existing_field[0]}"
                        )
                else:
                    all_fields[field_name] = (type_.__name__, field_type)

        columns_mapping = {"_type": "_type", "_key": "_key"}

        for field_name, (class_name, _) in all_fields.items():
            field_name = (
                field_name if not self.pascalize_column_names else camelize(field_name, uppercase_first_letter=True)
            )

            column_name = (
                f"{class_name}." if self.add_class_to_column_names and class_name is not None else ""
            ) + field_name

            columns_mapping[field_name] = column_name

        return columns_mapping

    # TODO (Roman): move to Schema
    @staticmethod
    def get_subtype_names(type_: Type) -> Set[str]:
        return set(schema_type.__name__ for schema_type in Schema.get_types() if type_ in schema_type.__mro__)
