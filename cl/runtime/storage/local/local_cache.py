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
from itertools import groupby

from cl.runtime import DataSource
from cl.runtime.records.record_annotations import GenericQuery
from cl.runtime.storage.data_source import GenericKey
from cl.runtime.storage.data_source import GenericRecord
from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Type


@dataclass(slots=True, init=True, frozen=True)
class LocalCache(DataSource):
    """Data source based on in-memory cache using Python dict."""

    _cache: Dict[str, Dict[Type, Dict[Tuple, Any]]] = field(default_factory=dict)

    def batch_size(self) -> int:
        """Maximum number or records the data source will return in a single call, error if exceeded."""
        return 1000000

    def load_unordered(
        self,
        keys: Iterable[GenericKey],
        dataset: List[str] | str | None = None,
    ) -> Iterable[GenericRecord]:
        # Try to retrieve dataset dictionary, insert if it does not yet exist
        dataset_cache = self._cache.setdefault(dataset, {})

        # Group keys by base type
        grouped_keys = groupby(keys, key=lambda x: x[0].get_base_type())

        # Process separately for each base type
        result_dict = []
        for base_type, keys_for_base_type in grouped_keys:

            # Try to retrieve table dictionary, insert if it does not yet exist
            table_cache = dataset_cache.setdefault(base_type, {})

            # Accumulate loaded (key, record) pairs
            result_dict.extend((x, table_cache[x[1:]]) for x in keys_for_base_type if x[1:] in table_cache)

        # Report error when record type is not a subclass of the respective key type
        not_subclass_records = [(k, v) for k, v in result_dict if not issubclass(v[0][0], k[0])]
        if len(not_subclass_records) > 0:
            not_subclass_records = not_subclass_records[:5]  # Report the first 5 errors
            pair_reports_str = "\n".join(
                [f"key_type={k[0].__name__} record_type={v[0][0].__name__}" for k, v in not_subclass_records]
            )
            raise RuntimeError(
                f"In method `load_unordered`, for the following (key_type, record_type) pairs "
                f"record_type is not a subclass of key_type:\n{pair_reports_str}\n")

        # Discard keys and return the records
        result = [v for k, v in result_dict]
        return result

    def load_by_query(
        self,
        query: GenericQuery,
        dataset: List[str] | str | None = None,
    ) -> Iterable[GenericRecord]:
        raise NotImplementedError()

    def save_many(
        self,
        records: Iterable[GenericRecord],
        dataset: List[str] | str | None = None,
    ) -> None:
        # Try to retrieve dataset dictionary, insert if it does not yet exist
        dataset_cache = self._cache.setdefault(dataset, {})

        # Group records by base type
        grouped_records = groupby(records, key=lambda record: record[0][0].get_base_type())

        # Process separately for each base type
        for base_type, records_for_base_type in grouped_records:
    
            # Try to retrieve table dictionary using `base_type` as key, insert if it does not yet exist
            table_cache = dataset_cache.setdefault(base_type, {})
    
            # Create a dict of new records using primary key fields tuple as key
            saved_records = {record[0][1:]: record for record in records_for_base_type}

            # Update table cache, adding records and overwriting existing records with saved records
            table_cache.update(saved_records)

    def delete_many(
        self,
        keys: Iterable[Tuple],
        dataset: List[str] | str | None = None,
    ) -> None:
        raise NotImplementedError()

    def delete_db(self) -> None:
        raise NotImplementedError()
