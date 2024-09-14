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

import pymongo
import re
from bson import UuidRepresentation
from cl.runtime.context.context import Context
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.storage.data_source import DataSource
from cl.runtime.storage.data_source_types import TQuery
from cl.runtime.storage.mongo.mongo_filter_serializer import MongoFilterSerializer
from cl.runtime.storage.protocols import TRecord
from dataclasses import dataclass
from itertools import groupby
from pymongo import MongoClient
from pymongo.database import Database
from typing import Dict
from typing import Iterable
from typing import Type
from typing import cast

invalid_db_name_symbols = r'/\\. "$*<>:|?'
"""Invalid MongoDB database name symbols."""

invalid_db_name_regex = re.compile(f"[{invalid_db_name_symbols}]")
"""Precompiled regex to check for invalid MongoDB database name symbols."""

# TODO: Revise and consider making fields of the data source
# TODO: Review and consider alternative names, e.g. DataSerializer or RecordSerializer
data_serializer = DictSerializer()
key_serializer = StringSerializer()
filter_serializer = MongoFilterSerializer()

_client_dict: Dict[str, MongoClient] = {}
"""Dict of MongoClient instances with client_uri key stored outside the class to avoid serializing them."""

_db_dict: Dict[str, Database] = {}
"""Dict of Database instances with client_uri.database_name key stored outside the class to avoid serializing them."""


@dataclass(slots=True, kw_only=True)
class BasicMongoDataSource(DataSource):
    """MongoDB data source without datasets."""

    client_uri: str = "mongodb://localhost:27017/"
    """MongoDB client URI, defaults to mongodb://localhost:27017/"""

    def load_one(
        self,
        record_type: Type[TRecord],
        record_or_key: TRecord | KeyProtocol | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> TRecord | None:
        if record_or_key is None or getattr(record_or_key, "get_key", None) is not None:
            # Record or None, return without lookup
            return cast(RecordProtocol, record_or_key)

        elif getattr(record_or_key, "get_key_type"):
            # Confirm dataset and identity are both None
            if dataset is not None:
                raise RuntimeError("BasicMongo data source type does not support datasets.")
            if identity is not None:
                raise RuntimeError("BasicMongo data source type does not support row-level security.")

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
        result = [self.load_one(record_type, x, dataset=dataset, identity=identity) for x in records_or_keys]
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
            raise RuntimeError("BasicMongo data source type does not support datasets.")
        if identity is not None:
            raise RuntimeError("BasicMongo data source type does not support row-level security.")

        # Key, get collection name from key type by removing Key suffix if present
        key_type = record_type.get_key_type()
        collection_name = key_type.__name__  # TODO: Decision on short alias
        db = self._get_db()
        collection = db[collection_name]

        serialized_records = collection.find()  # TODO: Filter by derived type
        result = []
        for serialized_record in serialized_records:
            del serialized_record["_id"]
            del serialized_record["_key"]
            record = data_serializer.deserialize_data(
                serialized_record
            )  # TODO: Convert to comprehension for performance
            result.append(record)
        return result

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
            raise RuntimeError("BasicMongo data source type does not support datasets.")
        if identity is not None:
            raise RuntimeError("BasicMongo data source type does not support row-level security.")

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

        # Confirm dataset and identity are both None
        if dataset is not None:
            raise RuntimeError("BasicMongo data source type does not support datasets.")
        if identity is not None:
            raise RuntimeError("BasicMongo data source type does not support row-level security.")

        # Get collection name from key type by removing Key suffix if present
        key_type = record.get_key_type()
        collection_name = key_type.__name__  # TODO: Decision on short alias
        db = self._get_db()
        collection = db[collection_name]

        # Serialize record data and key
        serialized_key = key_serializer.serialize_key(record)
        serialized_record = data_serializer.serialize_data(record)

        # Use update_one with upsert=True to insert if not present or update if present
        collection.update_one({"_key": serialized_key}, {"$set": serialized_record}, upsert=True)

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

        # Convert to (key_type, serialized_key, serialized_record) triples
        serialized_data = [
            (x.get_key_type(), key_serializer.serialize_key(x), data_serializer.serialize_data(x)) for x in records
        ]

        # Group by key_type
        grouped_data = groupby(serialized_data, key=lambda x: x[0])

        # Process separately for each base type
        for key_type, data_for_key_type in grouped_data:
            pass

    def delete_many(
        self,
        keys: Iterable[KeyProtocol] | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        # Validate the dataset and if necessary convert to delimited string
        raise NotImplementedError()

    def delete_all_and_drop_db(self) -> None:
        # Check that data_source_id and db_name both match temp_db_prefix
        db_name = self._get_db_name()
        Context.error_if_not_temp_db(self.data_source_id)
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
        db_key = f"{self.client_uri}.{db_name}"
        if (result := _db_dict.get(db_key, None)) is None:
            # Create if it does not exist
            client = self._get_client()
            # TODO: Implement dispose logic
            result = client[db_name]
            _db_dict[db_key] = result
        return result

    def _get_db_name(self) -> str:
        """Database is from data_source_id, check validity before returning."""
        result = self.data_source_id
        self.check_data_source_id(result)
        return result

    @classmethod
    def check_data_source_id(cls, data_source_id: str) -> None:
        """Check that data_source_id follows MongoDB database name restrictions, error message otherwise."""

        # Check for invalid characters in MongoDB name
        if invalid_db_name_regex.search(data_source_id):
            raise RuntimeError(
                f"MongoDB data_source_id='{data_source_id}' is not valid because it contains "
                f"special characters from this list: {invalid_db_name_symbols}"
            )

        # Check for maximum byte length of less than 64 (use Unicode bytes, not string chars to count)
        max_bytes = 63
        actual_bytes = len(data_source_id.encode("utf-8"))
        if actual_bytes > max_bytes:
            raise RuntimeError(
                f"MongoDB does not support data_source_id='{data_source_id}' because "
                f"it has {actual_bytes} bytes, exceeding the maximum of {max_bytes}."
            )
