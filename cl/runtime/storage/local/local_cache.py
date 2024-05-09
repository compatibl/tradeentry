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
from cl.runtime.records.record_annotations import GenericQuery, GenericOrder
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
        base_type: Type,
        keys: Iterable[GenericKey],
        dataset: List[str] | str | None = None,
    ) -> Iterable[GenericRecord]:
        # Try to retrieve dataset dictionary, insert if it does not yet exist
        dataset_cache = self._cache.setdefault(dataset, {})

        # Try to retrieve table dictionary, insert if it does not yet exist
        table_cache = dataset_cache.setdefault(base_type, {})

        result = []
        for key in keys:  # TODO: Accelerate by avoiding for loop
            # Separate type parameter which is the leading tuple element
            key_type = key[0]
            key_fields = key[1:]

            # Check that key_type is a subclass of base_type
            if not issubclass(key_type, base_type):
                key_fields_str_list = [str(k) for k in key_fields]
                raise RuntimeError(
                    f"In method `save_many`,"
                    f"`key_type={key_type.__name__}` is not a subclass of `base_type={base_type.__name__}` "
                    f"specified with key fields `{';'.join(key_fields_str_list)}`"
                )

            # Retrieve the record from table cache using get method
            # Will return None if the key is not found
            record = table_cache.get(key_fields)

            # Only add if the result is not None
            if record is not None:
                record_key, record_data = record
                record_type = record_key[0]

                # Check that record_type is a subclass of key_type
                if not issubclass(record_type, key_type):
                    key_fields_str_list = [str(k) for k in key_fields]
                    raise RuntimeError(
                        f"In method `load_unordered`,"
                        f"`record_type={record_type.__name__}` is not a subclass of `key_type={key_type.__name__}` "
                        f"specified with key fields `{';'.join(key_fields_str_list)}`"
                    )
                result.append(record)

        return result

    def load_by_query(
        self,
        base_type: Type,
        match_type: Type,
        query: GenericQuery | None,
        order: GenericOrder | None = None,
        dataset: List[str] | str | None = None,
    ) -> Iterable[GenericRecord]:
        raise NotImplementedError()

    def save_many(
        self,
        base_type: Type,
        records: Iterable[GenericRecord],
        dataset: List[str] | str | None = None,
    ) -> None:
        # Try to retrieve dataset dictionary, insert if it does not yet exist
        dataset_cache = self._cache.setdefault(dataset, {})

        # Try to retrieve table dictionary, insert if it does not yet exist
        table_cache = dataset_cache.setdefault(base_type, {})

        # Iterate over key-record pairs
        for record in records:
            # Parse generic record data
            key = record[0]
            key_type = key[0]
            key_fields = key[1:]

            if not issubclass(key_type, base_type):
                key_fields_str_list = [str(k) for k in key_fields]
                raise RuntimeError(
                    f"In method `save_many`,"
                    f"`key_type={key_type.__name__}` is not a subclass of `base_type={base_type.__name__}` "
                    f"specified with key fields `{';'.join(key_fields_str_list)}`"
                )

            # TODO: Support tables
            # Insert the record into dataset dictionary
            table_cache[key_fields] = record

    def delete_many(
        self,
        base_type: Type,
        keys: Iterable[Tuple],
        dataset: List[str] | str | None = None,
    ) -> None:
        raise NotImplementedError()

    def delete_db(self) -> None:
        raise NotImplementedError()
