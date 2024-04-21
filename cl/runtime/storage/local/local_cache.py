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
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.records.record_mixin import RecordMixin
from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Type
from cl.runtime.storage.data_source import RecordType, KeyType

@dataclass(slots=True, init=True, frozen=True)
class LocalCache(DataSource):
    """Data source based on in-memory cache using Python dict."""

    _cache: Dict[str, Dict] = field(default_factory=dict)

    def batch_size(self) -> int:
        """Maximum number or records the data source will return in a single call, error if exceeded."""
        return 1000000

    def load_unordered(
        self,
        keys: Iterable[KeyType],
        dataset: List[str] | str | None = None,
    ) -> Iterable[RecordType]:
        result = []
        for key in keys:  # TODO: Accelerate by avoiding for loop
            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(dataset, {})

            # Retrieve the record using get method that returns None if the key is not found
            record = dataset_cache.get(key)

            # Only add if the result is not None
            if record is not None:
                type_, dict_ = record
                result.append((key, type_, dict_))

        return result

    def load_by_query(
        self,
        base_type: Type,
        record_type: Type,
        query: Dict[str, Any] | None,
        order: Dict[str, int] | None = None,
        dataset: List[str] | str | None = None,
    ) -> Iterable[RecordType]:
        raise NotImplementedError()

    def save_many(
        self,
        records: Iterable[RecordType],
        dataset: List[str] | str | None = None,
    ) -> None:
        # Iterate over key-record pairs
        for key, type_, dict_ in records:
            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(dataset, {})

            # TODO: Support tables
            # Insert the record into dataset dictionary
            dataset_cache[key] = (type_, dict_)

    def delete_many(
        self,
        keys: Iterable[KeyType],
        dataset: List[str] | str | None = None,
    ) -> None:
        raise NotImplementedError()

    def delete_db(self) -> None:
        raise NotImplementedError()
