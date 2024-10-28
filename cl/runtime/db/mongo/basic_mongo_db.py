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

import re
from dataclasses import dataclass
from typing import Dict
from typing import Iterable
from typing import Type
from typing import cast
from pymongo import MongoClient
from pymongo.database import Database
from cl.runtime.context.context import Context
from cl.runtime.db.db import Db
from cl.runtime.db.mongo.mongo_filter_serializer import MongoFilterSerializer
from cl.runtime.db.protocols import TKey
from cl.runtime.db.protocols import TRecord
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.records.record_util import RecordUtil
from cl.runtime.schema.schema import Schema
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer

invalid_db_name_symbols = r'/\\. "$*<>:|?'
"""Invalid MongoDB database name symbols."""

invalid_db_name_regex = re.compile(f"[{invalid_db_name_symbols}]")
"""Precompiled regex to check for invalid MongoDB database name symbols."""

# TODO: Revise and consider making fields of the database
# TODO: Review and consider alternative names, e.g. DataSerializer or RecordSerializer
data_serializer = DictSerializer()
key_serializer = StringSerializer()
filter_serializer = MongoFilterSerializer()

_client_dict: Dict[str, MongoClient] = {}
"""Dict of MongoClient instances with client_uri key stored outside the class to avoid serializing them."""

_db_dict: Dict[str, Database] = {}
"""Dict of database instances with client_uri.database_name key stored outside the class to avoid serializing them."""


@dataclass(slots=True, kw_only=True)
class BasicMongoDb(Db):
    """MongoDB database without datasets."""

    client_uri: str = "mongodb://localhost:27017/"
    """MongoDB client URI, defaults to mongodb://localhost:27017/"""

    def load_one(
        self,
        record_type: Type[TRecord],
        record_or_key: TRecord | KeyProtocol | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
        is_key_optional: bool = False,
        is_record_optional: bool = False,
    ) -> TRecord | None:
        # Check for an empty key
        if record_or_key is None:
            if is_key_optional:
                return None
            else:
                raise UserError(f"Key is None when trying to load record type {record_type.__name__} from DB.")

        if record_or_key is None or getattr(record_or_key, "get_key", None) is not None:
            # Record or None, return without lookup
            return cast(RecordProtocol, record_or_key)
        elif getattr(record_or_key, "get_key_type"):
            # Confirm dataset and identity are both None
            if dataset is not None:
                raise RuntimeError("BasicMongo database type does not support datasets.")
            if identity is not None:
                raise RuntimeError("BasicMongo database type does not support row-level security.")

            # Key, get collection name from key type by removing Key suffix if present
            key_type = record_or_key.get_key_type()
            collection_name = key_type.__name__  # TODO: Decision on short alias
            db = self._get_db()
            collection = db[collection_name]

            serialized_key = key_serializer.serialize_key(record_or_key)
            serialized_record = collection.find_one({"_key": serialized_key})
            if serialized_record is not None:
                del serialized_record["_id"]
                del serialized_record["_key"]
                result = data_serializer.deserialize_data(serialized_record)
                return result
            else:
                # Check if returning None is allowed
                if not is_record_optional:
                    raise UserError(f"{record_type.__name__} record is not found for key {record_or_key}")
                return None
        else:
            raise RuntimeError(f"Type {record_or_key.__class__.__name__} is not a record or key.")

    def load_many(
        self,
        record_type: Type[TRecord],
        records_or_keys: Iterable[TRecord | KeyProtocol | tuple | str | None] | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[TRecord | None] | None:
        # TODO: Implement directly for better performance
        result = [
            self.load_one(
                record_type,
                x,
                dataset=dataset,
                identity=identity,
                is_key_optional=True,  # TODO: Keep the existing defaults for load_many
                is_record_optional=True,  # TODO: Keep the existing defaults for load_many
            )
            for x in records_or_keys
        ]
        return result

    def load_all(
        self,
        record_type: Type[TRecord],
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[TRecord | None] | None:
        # Confirm dataset and identity are both None
        if dataset is not None:
            raise RuntimeError("BasicMongo database type does not support datasets.")
        if identity is not None:
            raise RuntimeError("BasicMongo database type does not support row-level security.")

        # Key, get collection name from key type by removing Key suffix if present
        key_type = record_type.get_key_type()
        collection_name = key_type.__name__  # TODO: Decision on short alias
        db = self._get_db()
        collection = db[collection_name]

        subtype_names = list(t.__name__ for t in Schema.get_type_successors(record_type))
        serialized_records = collection.find({"_type": {"$in": subtype_names}})
        result = []
        for serialized_record in serialized_records:
            del serialized_record["_id"]
            del serialized_record["_key"]
            record = data_serializer.deserialize_data(
                serialized_record
            )  # TODO: Convert to comprehension for performance
            result.append(record)
        return RecordUtil.sort_records_by_key(result)

    def load_filter(
        self,
        record_type: Type[TRecord],
        filter_obj: TRecord,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[TRecord]:
        # Confirm dataset and identity are both None
        if dataset is not None:
            raise RuntimeError("BasicMongo database type does not support datasets.")
        if identity is not None:
            raise RuntimeError("BasicMongo database type does not support row-level security.")

        # Key, get collection name from key type by removing Key suffix if present
        key_type = record_type.get_key_type()
        collection_name = key_type.__name__  # TODO: Decision on short alias
        db = self._get_db()
        collection = db[collection_name]

        # Convert filter object to a dictionary
        filter_dict = filter_serializer.serialize_filter(filter_obj)

        serialized_records = collection.find(filter_dict)  # TODO: Filter by derived type
        result = []
        for serialized_record in serialized_records:
            del serialized_record["_id"]
            del serialized_record["_key"]
            record = data_serializer.deserialize_data(
                serialized_record
            )  # TODO: Convert to comprehension for performance
            result.append(record)
        return result

    def save_one(
        self,
        record: RecordProtocol | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        # If record is None, do nothing
        if record is None:
            return

        # Call on_save if defined
        if hasattr(record, "on_save"):
            record.on_save()  # TODO: Refactor on_save

        # Confirm dataset and identity are both None
        if dataset is not None:
            raise RuntimeError("BasicMongo database type does not support datasets.")
        if identity is not None:
            raise RuntimeError("BasicMongo database type does not support row-level security.")

        # Get collection name from key type by removing Key suffix if present
        key_type = record.get_key_type()
        collection_name = key_type.__name__  # TODO: Decision on short alias
        db = self._get_db()
        collection = db[collection_name]

        # Serialize data, this also executes 'init_all' method
        serialized_record = data_serializer.serialize_data(record)

        # Serialize key
        # TODO: Consider getting the key first instead of serializing the entire record
        serialized_key = key_serializer.serialize_key(record)

        # Use update_one with upsert=True to insert if not present or update if present
        # TODO (Roman): update_one does not affect fields not presented in record. Changed to replace_one
        serialized_record["_key"] = serialized_key
        collection.replace_one({"_key": serialized_key}, serialized_record, upsert=True)

    def save_many(
        self,
        records: Iterable[RecordProtocol],
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        # TODO: Temporary, replace by independent implementation
        [self.save_one(x, dataset=dataset, identity=identity) for x in records]
        return

    def delete_one(
        self,
        key_type: Type[TKey],
        key: TKey | KeyProtocol | tuple | str | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        # Confirm dataset and identity are both None
        if dataset is not None:
            raise RuntimeError("BasicMongo database type does not support datasets.")
        if identity is not None:
            raise RuntimeError("BasicMongo database type does not support row-level security.")

        # Get collection name from key type by removing Key suffix if present
        collection_name = key_type.__name__  # TODO: Decision on short alias
        db = self._get_db()
        collection = db[collection_name]

        serialized_key = key_serializer.serialize_key(key)

        delete_filter = {"_key": serialized_key}
        collection.delete_one(delete_filter)

    def delete_many(
        self,
        keys: Iterable[KeyProtocol] | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        for key in keys:
            self.delete_one(type(key), key, dataset=dataset, identity=identity)

    def delete_all_and_drop_db(self) -> None:
        # Check that db_id and db_name both match temp_db_prefix
        db_name = self._get_db_name()
        Context.error_if_not_temp_db(self.db_id)
        Context.error_if_not_temp_db(db_name)

        # Drop the entire database without possibility of recovery, this
        # relies on the temp_db_prefix check above to prevent unintended use
        client = self._get_client()
        client.drop_database(db_name)

    def close_connection(self) -> None:
        if (client := _client_dict.get(self.client_uri, None)) is not None:
            # Close connection
            client.close()
            # Remove client from dictionary so connection can be reopened on next access
            del _client_dict[self.client_uri]

    def _get_client(self) -> MongoClient:
        """Get PyMongo client object."""
        if (client := _client_dict.get(self.client_uri, None)) is None:
            # Create if it does not exist
            client = MongoClient(
                self.client_uri,
                uuidRepresentation="standard",
            )
            # TODO: Implement dispose logic
            _client_dict[self.client_uri] = client
        return client

    def _get_db(self) -> Database:
        """Get PyMongo database object."""
        db_name = self._get_db_name()
        db_key = f"{self.client_uri}{db_name}"
        if (result := _db_dict.get(db_key, None)) is None:
            # Create if it does not exist
            client = self._get_client()
            # TODO: Implement dispose logic
            result = client[db_name]
            _db_dict[db_key] = result
        return result

    def _get_db_name(self) -> str:
        """Database is from db_id, check validity before returning."""
        result = self.db_id
        self.check_db_id(result)
        return result

    @classmethod
    def check_db_id(cls, db_id: str) -> None:
        """Check that db_id follows MongoDB database name restrictions, error message otherwise."""

        # Check for invalid characters in MongoDB name
        if invalid_db_name_regex.search(db_id):
            raise RuntimeError(
                f"MongoDB db_id='{db_id}' is not valid because it contains "
                f"special characters from this list: {invalid_db_name_symbols}"
            )

        # Check for maximum byte length of less than 64 (use Unicode bytes, not string chars to count)
        max_bytes = 63
        actual_bytes = len(db_id.encode("utf-8"))
        if actual_bytes > max_bytes:
            raise RuntimeError(
                f"MongoDB does not support db_id='{db_id}' because "
                f"it has {actual_bytes} bytes, exceeding the maximum of {max_bytes}."
            )

    # TODO (Roman): move to base Db class?
    def is_empty(self) -> bool:
        """Return True if db has no collections."""
        return len(self._get_db().list_collection_names()) == 0
