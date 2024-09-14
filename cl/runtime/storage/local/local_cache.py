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

from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.storage.data_source_types import TQuery
from cl.runtime.storage.dataset_util import DatasetUtil
from cl.runtime.storage.protocols import TKey
from cl.runtime.storage.protocols import TRecord
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import Dict
from typing import Iterable
from typing import Type
from typing import cast
from typing_extensions import Self

key_serializer = StringSerializer()
"""Serializer for keys used in cache lookup."""

_local_cache_instance: LocalCache | None = None
"""Singleton instance is created on first access."""


@dataclass(slots=True, kw_only=True)
class LocalCache:
    """In-memory cache for objects without serialization."""

    __cache: Dict[KeyProtocol, RecordProtocol] = field(default_factory=lambda: {})
    """Record instance is stored in cache without serialization."""

    def load_one(
        self,
        record_type: Type[TRecord],
        record_or_key: TRecord | KeyProtocol | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> TRecord | None:
        if record_or_key is None or getattr(record_or_key, "get_key", None) is not None:
            # Key instance is Record or None, return without lookup
            return cast(RecordProtocol, record_or_key)

        elif getattr(record_or_key, "get_key_type"):
            # Key, look up the record in cache
            key_type = record_or_key.get_key_type()
            serialized_key = key_serializer.serialize_key(record_or_key)

            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self.__cache.setdefault(dataset, {})

            # Try to retrieve table dictionary, return None if not found
            if (table_cache := dataset_cache.setdefault(key_type, None)) is None:
                return None

            # Look up the record, return None if not found
            result = table_cache.get(serialized_key, None)
            return result

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
        raise NotImplementedError()

    def load_filter(
        self,
        record_type: Type[TRecord],
        filter_obj: TRecord,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[TRecord]:
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

        # Try to retrieve dataset dictionary, insert if it does not yet exist
        dataset_cache = self.__cache.setdefault(dataset, {})

        # Try to retrieve table dictionary using 'key_type' as key, insert if it does not yet exist
        key_type = record.get_key_type()
        table_cache = dataset_cache.setdefault(key_type, {})

        # Serialize both key and record
        serialized_key = key_serializer.serialize_key(record)

        # Add record to cache, overwriting an existing record if present
        table_cache[serialized_key] = record

    def save_many(
        self,
        records: Iterable[RecordProtocol],
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        # TODO: Review performance compared to a custom implementation for save_many
        [self.save_one(x) for x in records]

    def delete_one(
        self,
        key_type: Type[TKey],
        key: TKey | KeyProtocol | tuple | str | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        raise NotImplementedError()

    def delete_many(
        self,
        keys: Iterable[KeyProtocol] | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        # Validate the dataset and if necessary convert to delimited string
        raise NotImplementedError()

    @classmethod
    def instance(cls) -> Self:
        """Return singleton instance."""

        # Check if cached value exists, load if not found
        global _local_cache_instance
        if _local_cache_instance is None:
            # Create if does not yet exist
            _local_cache_instance = LocalCache()
        return _local_cache_instance
