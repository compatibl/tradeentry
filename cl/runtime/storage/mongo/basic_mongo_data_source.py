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

from bson import UuidRepresentation
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.storage.data_source import DataSource
from cl.runtime.storage.data_source_types import TQuery
from cl.runtime.storage.protocols import TRecord
from dataclasses import dataclass
from dataclasses import field
from itertools import groupby
from pymongo import MongoClient
from pymongo.database import Database
from typing import Iterable
from typing import Type
from typing import cast

# TODO: Revise and consider making fields of the data source
data_serializer = DictSerializer()
key_serializer = StringSerializer()


@dataclass(slots=True, kw_only=True)
class BasicMongoDataSource(DataSource):
    """MongoDB data source without datasets."""

    db_name: str = missing()
    """Database name must be unique for each DB client."""

    client_uri: str = "mongodb://localhost:27017/"
    """MongoDB client URI, defaults to mongodb://localhost:27017/"""

    _client: MongoClient = None
    """MongoDB client, tests must specify mongomock.MongoClient."""

    _db: Database = field(default=None, init=False)
    """MongoDB database."""

    def __post_init__(self) -> None:
        """Initialize private attributes."""

        client = MongoClient(
            self.client_uri,
            uuidRepresentation="standard",
        )

        # TODO: Implement dispose logic
        # Use setattr to initialize attributes in a frozen object
        if self._client is None:
            object.__setattr__(self, "_client", client)
        object.__setattr__(self, "_db", self._client[self.db_name])

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
            collection = self._db[collection_name]

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
        collection = self._db[collection_name]

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

    def load_by_query(
        self,
        query: TQuery,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[RecordProtocol]:
        # Validate the dataset and if necessary convert to delimited string
        raise NotImplementedError()

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
        collection = self._db[collection_name]

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

    def delete_all(self) -> None:
        raise NotImplementedError()
