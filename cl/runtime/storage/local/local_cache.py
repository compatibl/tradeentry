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
from cl.runtime.storage.data_source_types import TDataset
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


@dataclass(slots=True, kw_only=True, init=True, frozen=True)
class LocalCache(DataSource):
    """Data source based on in-memory cache using Python dict."""

    _cache: Dict[str, Dict[Type, Dict[Tuple, Any]]] = field(default_factory=dict)

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

        # Group keys by base type
        grouped_keys = groupby(keys, key=lambda x: x[0])

        # Process separately for each base type
        result_dict = {}
        for base_type, keys_for_base_type in grouped_keys:
            # Try to retrieve table dictionary, insert if it does not yet exist
            table_cache = dataset_cache.setdefault(base_type, {})

            # Iterable for the retrieved pairs
            retrieved = {x: table_cache.get(x[1:], None) for x in keys_for_base_type}
            result_dict.update(retrieved)

        # Report error when record type is not a subclass of the respective key type
        not_subclass_records = [(k, v) for k, v in result_dict.items() if not issubclass(v[0][0], k[0])]
        if len(not_subclass_records) > 0:
            not_subclass_records = not_subclass_records[:5]  # Report the first 5 errors
            pair_reports_str = "\n".join(
                [
                    f"record_type={v[0][0].__name__} key_type={k[0].__name__} key={';'.join(k[1:])} "
                    for k, v in not_subclass_records
                ]
            )
            raise RuntimeError(
                f"In method `load_many`, record_type is not a subclass of key_type "
                f"for the following records:\n{pair_reports_str}\n"
            )

        # Records in the order of provided keys, None is added to list if the record is not found
        result = [result_dict.get(k, None) for k in keys]
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
        grouped_records = groupby(packs, key=lambda record: record[0][0])

        # Process separately for each base type
        for base_type, records_for_base_type in grouped_records:
            # Try to retrieve table dictionary using `base_type` as key, insert if it does not yet exist
            table_cache = dataset_cache.setdefault(base_type, {})

            # Create a dict of records for base type using primary key fields as dict key
            # Type is excluded from dict key because it is the final type, and may vary
            # within the table
            saved_records = {record[0][1:]: record for record in records_for_base_type}

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

    def delete_db(self) -> None:
        raise NotImplementedError()
