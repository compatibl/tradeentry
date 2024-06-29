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
from cl.runtime.storage.data_source import TKey
from cl.runtime.storage.data_source import TLoadedRecord
from cl.runtime.storage.data_source_types import TDataset, TData
from cl.runtime.storage.data_source_types import TIdentity
from cl.runtime.storage.data_source_types import TPackedRecord
from cl.runtime.storage.data_source_types import TQuery
from cl.runtime.storage.dataset_util import DatasetUtil
from dataclasses import dataclass
from dataclasses import field
from itertools import groupby
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Tuple
from typing import Type


@dataclass(slots=True, kw_only=True, frozen=True)
class LocalCache(DataSource):
    """Data source based on in-memory cache using Python dict."""

    _cache: Dict[str, Dict[Type, Dict[TKey, TData]]] = field(default_factory=dict)

    def batch_size(self) -> int:
        """Maximum number or records the data source will return in a single call, error if exceeded."""
        return 1000000

    def load_many(
        self,
        keys: Iterable[TKey],
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> Iterable[TLoadedRecord]:
        # Validate the dataset and if necessary convert to delimited string
        dataset = DatasetUtil.to_str(dataset)

        # Try to retrieve dataset dictionary, insert if it does not yet exist
        dataset_cache = self._cache.setdefault(dataset, {})

        # Group keys by key type
        keys_grouped_by_key_type = groupby(keys, key=lambda x: type(x))

        # Process separately for each base type
        result_dict = {}
        for key_type, keys_for_key_type in keys_grouped_by_key_type:
            # Try to retrieve table dictionary, insert if it does not yet exist
            table_cache = dataset_cache.setdefault(key_type, {})

            # Iterable for the retrieved pairs
            key_tuples = [key.get_key_tuple() for key in keys_for_key_type]
            retrieved = {key_tuple: table_cache[key_tuple] for key_tuple in key_tuples if key_tuple in table_cache}
            result_dict.update(retrieved)

        # Records in the order of provided keys, or None for records that are not found
        result = [(k, result_dict[k.get_key_tuple()], dataset, None) if k.get_key_tuple() in result_dict else None for k in keys]
        return result

    def load_by_query(
        self,
        query: TQuery,
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> Iterable[TLoadedRecord]:
        # Validate the dataset and if necessary convert to delimited string
        dataset = DatasetUtil.to_str(dataset)

        raise NotImplementedError()

    def save_many(
        self, packs: Iterable[TPackedRecord], *, dataset: TDataset = None, identity: TIdentity = None
    ) -> None:
        # Validate the dataset and if necessary convert to delimited string
        dataset = DatasetUtil.to_str(dataset)

        # Try to retrieve dataset dictionary, insert if it does not yet exist
        dataset_cache = self._cache.setdefault(dataset, {})

        # Group records by base type
        packs_grouped_by_table_type = groupby(packs, key=lambda record: type(record[0]))

        # Process separately for each base type
        for table_type, packs_for_table_type in packs_grouped_by_table_type:
            # Try to retrieve table dictionary using `table_type` as key, insert if it does not yet exist
            table_cache = dataset_cache.setdefault(table_type, {})

            # Create a dict of (key, data)
            saved_records = {pack[0].get_key_tuple(): pack[1] for pack in packs_for_table_type}

            # Add records for base type, overwriting the existing records
            table_cache.update(saved_records)

    def delete_many(
        self,
        keys: Iterable[TKey],
        *,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> None:
        # Validate the dataset and if necessary convert to delimited string
        dataset = DatasetUtil.to_str(dataset)
        raise NotImplementedError()

    def delete_db(self) -> None:
        raise NotImplementedError()
