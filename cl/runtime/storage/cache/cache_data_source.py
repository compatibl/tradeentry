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

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional, Type, Union

from cl.runtime.core.storage.data_source import DataSource, TKey, TRecord
from cl.runtime.core.storage.record import Record
from cl.runtime.core.storage.record_util import RecordUtil


@dataclass
class CacheDataSource(DataSource):
    """Data source based on in-memory cache using Python dict."""

    _cache: Dict[str, Dict] = field(default_factory=dict)  # TODO: switch to class_field and remove the default factory

    def init(self) -> None:
        """Validate dataclass attributes and use them to initialize object state."""

        # Create new cache on init
        self._cache = {}

    def load_many(
        self,
        base_type: Type[TRecord],
        keys: Iterable[Union[str, TKey]],
        data_set: str,
        *,
        is_optional: bool = None,
        is_optional_key: bool = None,
        is_unordered: bool = None,
    ) -> Iterable[TRecord]:
        """
        Load instances of classes derived from base_type from storage using a sequence of keys.

        - Parameter `base_type` determines the database table where the search is performed.
        - Error message if a loaded record is not derived from `base_type`.
        - The order of results is the same as the order of argument keys unless `is_unordered` is set.
        - To avoid saving and then loading the records that are created in memory, any argument key that
          is itself derived from base_type will be returned bypassing the data source query.
          Call `get_key()` on keys before passing them as argument to avoid this behavior.

        Args:
            base_type: Loaded records must be derived from `base_type`
            keys: Sequence of string keys or key classes for which records will be loaded.
            data_set: Directory-like attribute used to organize the data.
            is_optional: Return None if the record is not found. Default is to raise an error.
            is_optional_key: Return None if a key is None. Default is to raise an error.
            is_unordered: Do not order result in the order of keys. Default is to order the result.
        """

        result = []
        for key in keys:
            if key is None:
                # Handle key=None
                if is_optional_key:
                    result.append(None)
                    continue
                else:
                    raise RuntimeError("Key=None but 'is_optional_key' not set.")
            elif isinstance(key, Record):
                # Handle full record passed instead of the key
                result.append(key)
                continue
            elif isinstance(key, str):
                key = key
            else:
                raise RuntimeError(f'Key {key} is not a string, Key, or Record')

            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(data_set, {})

            # Retrieve the record using get method that returns None if the key is not found
            record_dict = dataset_cache.get(key)

            # Check if result is None
            if record_dict is None:
                if is_optional:
                    result.append(None)
                    continue
                else:
                    raise RuntimeError(
                        f"Record is not found for key={key} but 'is_optional' argument is False or None."
                    )

            # Create record instance and populate it from dictionary
            # Final type name is the last element of type discriminators list
            type_discriminators = record_dict['_t']
            class_path = type_discriminators[0]
            module_path, class_name = RecordUtil.split_class_path(class_path)

            class_ = RecordUtil.get_class_type(module_path, class_name)
            record = class_()
            record.from_dict(record_dict)

            # Validate attributes and initialize object state
            record.init()

            # Verify that the record has the same key as was passed to the load method
            record_key = record.get_key()
            if record_key != key:
                raise RuntimeError(
                    f'Record get_key() method returns {record_key} which does '
                    f'not match the argument {key} passed to the load method.'
                )

            # TODO - refactor to improve speed
            result.append(record)

        return result

    def save_many(self, records: Iterable[Record], data_set: str) -> None:
        """
        Save many records to the specified dataset, bypassing the commit
        queue and using save options if provided (see SaveOptions
        class for details).

        This method does not implicitly call commit(). The commit queue
        will remain in its original state after the method exits.
        """

        # Iterate over records
        for record in records:
            # Validate attributes and update object state before saving
            record.init()

            # Get primary key and data from record.
            key = record.get_key()
            record_dict = record.to_dict()

            # Make deep copy of dictionary in case the original record is changed
            # while the dictionary is persisted in cache
            record_dict = deepcopy(record_dict)

            # Add the list of types from base to derived
            record_dict["_t"] = RecordUtil.get_inheritance_chain(type(record))

            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(data_set, {})

            # TODO: Support tables
            # Insert the record into dataset dictionary
            common_base = record.get_common_base()  # noqa
            table_name = RecordUtil.get_class_path(common_base)
            dataset_cache[key] = record_dict

    def save_on_commit(self, record: Record, data_set: str) -> None:
        """
        Add the record to the commit queue.

        The record will not be saved until a call to commit() which
        executes all pending requests in the commit queue. Alternatively,
        rollback() may be used to clear the commit queue without executing
        the pending requests.
        """
        raise NotImplementedError()

    def delete_many(self, keys: Iterable[Record], data_set: str) -> None:
        """
        Delete many records in the specified dataset, bypassing
        the commit queue. If an element of the 'keys' argument is
        a full record, only its key will be used.

        This method does not implicitly call commit(). The commit queue
        will remain in its original state after the method exits.

        Depending on data source implementation, this method may
        delete a record or write the delete marker (DeletedRecord)
        to shadow previous versions of the record or records with
        the same key in a parent dataset. This ensures that records
        with the same primary key in dataset and/or data source lookup
        chain do not become visible after this record is deleted.
        """
        raise NotImplementedError()

    def delete_on_commit(self, key: Record, data_set: str) -> None:
        """
        Add to commit queue the command to delete record in the
        specified dataset. No error is raised if the record does not
        exist. If the 'key' argument is a full record, only its
        key will be used.

        The record will not be saved until a call to commit() which
        executes all pending requests in the commit queue. Alternatively,
        rollback() may be used to clear the commit queue without executing
        the pending requests.

        Depending on data source implementation, this method may
        delete a record or write the delete marker (DeletedRecord)
        to shadow previous versions of the record or records with
        the same key in a parent dataset. This ensures that records
        with the same primary key in dataset and/or data source lookup
        chain do not become visible after this record is deleted.
        To avoid an additional roundtrip to the data store, the delete
        marker may be written even when the record does not exist.
        """
        raise NotImplementedError()

    def commit(self) -> None:
        """
        Execute all pending save and delete requests in the commit queue
        and clear the queue.
        """
        raise NotImplementedError()

    def rollback(self) -> None:
        """
        Clear the commit queue without executing the pending save and delete
        requests in the queue.
        """
        raise NotImplementedError()

    def delete_db(self) -> None:
        """
        Permanently deletes (drops) the database with all records
        in it without the possibility to recover them later.

        This method should only be used to free storage. For
        all other purposes, methods that preserve history should
        be used.

        ATTENTION - THIS METHOD WILL DELETE ALL DATA WITHOUT
        THE POSSIBILITY OF RECOVERY. USE WITH CAUTION.
        """
        raise NotImplementedError()
