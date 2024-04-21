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

from dataclasses import dataclass, field

from cl.runtime import DataSource
from dataclasses import dataclass
from cl.runtime.classes.dataclasses.dataclass_mixin import data_field
from cl.runtime.classes.record_mixin import RecordMixin
from cl.runtime.classes.class_info import ClassInfo
from copy import deepcopy
from typing import Dict, Tuple, List, Any
from typing import Iterable
from typing import Type
from typing import TypeVar
from typing import Union

TKey = TypeVar("TKey", contravariant=True)
TRecord = TypeVar("TRecord", covariant=True)


@dataclass(slots=True, init=True, frozen=True)
class LocalCache(DataSource):
    """Data source based on in-memory cache using Python dict."""

    _cache: Dict[str, Dict] = field(default_factory=dict)

    def batch_size(self) -> int:
        """Maximum number or records the data source will return in a single call, error if exceeded."""
        return 1000000

    def load_unordered(
            self,
            keys: Iterable[Tuple],
            dataset: List[str] | str | None = None,
    ) -> Iterable[Tuple[Tuple, Type, Dict[str, Any]]]:

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

    def save_many(
        self,
        key_record_pairs: Iterable[Tuple[Tuple, Type, Dict[str, Any]]],
        dataset: List[str] | str | None = None,
    ) -> None:

        # Iterate over key-record pairs
        for key, type_, dict_ in key_record_pairs:

            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(dataset, {})

            # TODO: Support tables
            # Insert the record into dataset dictionary
            dataset_cache[key] = (type_, dict_)

    def load_by_query(
            self,
            table: str,
            query: Dict[str, Any] | None,
            order: Dict[str, int] | None = None,
            dataset: List[str] | str | None = None,
    ) -> Iterable[Dict[str, Any]]:
        raise NotImplementedError()

    def delete_many(
            self,
            table: str,
            keys: Iterable[Tuple],
            dataset: List[str] | str | None = None,
    ) -> None:
        raise NotImplementedError()

    def delete_db(self) -> None:
        raise NotImplementedError()