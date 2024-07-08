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

from cl.runtime import DataSource
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.serialization.slots_key_serializer import SlotsKeySerializer
from cl.runtime.serialization.slots_serializer import SlotsSerializer
from cl.runtime.storage.data_source_types import TData
from cl.runtime.storage.data_source_types import TDataset
from cl.runtime.storage.data_source_types import TIdentity
from cl.runtime.storage.data_source_types import TQuery
from cl.runtime.storage.dataset_util import DatasetUtil
from dataclasses import dataclass
from dataclasses import field
from itertools import groupby
from typing import Dict
from typing import Iterable
from typing import Type
from typing import cast

# TODO: Revise and consider making fields of the data source
data_serializer = SlotsSerializer()
key_serializer = SlotsKeySerializer()


@dataclass(slots=True, kw_only=True, frozen=True)
class LocalCache(DataSource):
    """Data source based on in-memory cache using Python dict."""

    _cache: Dict[str, Dict[Type, Dict[str, TData]]] = field(default_factory=dict)

    def batch_size(self) -> int:
        """Maximum number or records the data source will return in a single call, error if exceeded."""
        return 1000000

    def load_one(
        self,
        record_or_key: KeyProtocol | None,
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> RecordProtocol | None:
        if record_or_key is None or getattr(record_or_key, "get_key", None) is not None:
            # Record or None, return without lookup
            return cast(RecordProtocol, record_or_key)

        elif getattr(record_or_key, "get_key_type"):
            # Key, look up the record in cache
            key_type = record_or_key.get_key_type()
            serialized_key = key_serializer.serialize_key(record_or_key)

            # Validate the dataset and if necessary convert to delimited string
            dataset = DatasetUtil.to_str(dataset)

            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(dataset, {})

            # Try to retrieve table dictionary, return None if not found
            if (table_cache := dataset_cache.setdefault(key_type, None)) is None:
                return None

            # Look up the record, return None if not found
            if (serialized_record := table_cache[serialized_key]) is None:
                return None

            # Deserialize and return
            record = data_serializer.deserialize(serialized_record)
            return record

        else:
            raise RuntimeError(f"Type {record_or_key.__class__.__name__} is not a record or key.")

    def load_many(
        self,
        records_or_keys: Iterable[KeyProtocol | None] | None,
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> Iterable[RecordProtocol | None] | None:
        # TODO: Review performance compared to a custom implementation for load_many
        result = [self.load_one(x) for x in records_or_keys]
        return result

    def load_by_query(
        self,
        query: TQuery,
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> Iterable[RecordProtocol]:
        # Validate the dataset and if necessary convert to delimited string
        dataset = DatasetUtil.to_str(dataset)

        raise NotImplementedError()

    def save_one(self, record: RecordProtocol | None, *, dataset: TDataset = None, identity: TIdentity = None) -> None:
        # If record is None, do nothing
        if record is None:
            return

        # Validate the dataset and if necessary convert to delimited string
        dataset = DatasetUtil.to_str(dataset)

        # Try to retrieve dataset dictionary, insert if it does not yet exist
        dataset_cache = self._cache.setdefault(dataset, {})

        # Try to retrieve table dictionary using `key_type` as key, insert if it does not yet exist
        key_type = record.get_key_type()
        table_cache = dataset_cache.setdefault(key_type, {})

        # Serialize both key and record
        serialized_key = key_serializer.serialize_key(record)
        serialized_record = data_serializer.serialize(record)

        # Add record to cache, overwriting an existing record if present
        table_cache[serialized_key] = serialized_record

    def save_many(
        self, records: Iterable[RecordProtocol], *, dataset: TDataset = None, identity: TIdentity = None
    ) -> None:
        # TODO: Review performance compared to a custom implementation for save_many
        [self.save_one(x) for x in records]

    def delete_many(
        self,
        keys: Iterable[KeyProtocol] | None,
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> None:
        # Validate the dataset and if necessary convert to delimited string
        dataset = DatasetUtil.to_str(dataset)
        raise NotImplementedError()

    def delete_db(self) -> None:
        raise NotImplementedError()
