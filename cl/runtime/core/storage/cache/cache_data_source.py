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
from typing import Dict, Iterable, Union

from cl.runtime.core.storage.data_source import DataSource
from cl.runtime.core.storage.record import Record


@dataclass
class CacheDataSource(DataSource):
    """Data source based on in-memory cache using Python dict."""

    _cache: Dict[str, Dict] = field(default_factory=dict)

    def init(self) -> None:
        """Update and validate object state after loading from DB and before saving to DB."""

        # Create new cache on init
        self._cache = {}

    def load_many(
        self,
        keys: Iterable[Union[str, Record]],
        data_set: str,
        *,
        ignore_not_found: bool = False,
        ignore_null_key: bool = False,
        out: Iterable[Record]
    ) -> None:
        """
        Populate the collection of objects specified via the 'out' argument
        with data loaded from the specified dataset and collection of keys.
        If an element of the 'keys' argument is a full record, only its key
        will be used.
        """

        # TODO: Implement using zip(keys, out, strict=True) in Python 3.10
        key_list = list(keys)
        out_list = list(out)
        if len(key_list) != len(out_list):
            raise RuntimeError(f'In load_many(...), keys has length {len(key_list)} and out has length {len(out_list)}')

        # Iterate over keys and out in parallel after checking they have equal length
        zipped = zip(key_list, out_list)
        for key, out in zipped:
            # Handle key=None and check key type
            if key is None:
                if ignore_null_key:
                    return None
                else:
                    raise RuntimeError(
                        "Null key is passed to load_one(...) method but 'ignore_null_key' flag is not set."
                    )
            elif isinstance(key, str):
                pk = key
            elif isinstance(key, Record):
                pk = key.to_pk()
            else:
                raise RuntimeError('Key {key} is not a string, derived type of Record, or None')

            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(data_set, {})

            # Retrieve the record using get method that returns None if the key is not found
            record_dict = dataset_cache.get(pk)

            # Check if result is None
            if record_dict is None:
                if ignore_not_found:
                    return None
                else:
                    raise RuntimeError(
                        f"Record is not found for pk={pk} but 'ignore_not_found' flag is not set."
                    )

            # Populate record from dictionary
            out.from_dict(record_dict)

            # Call init to update and validate object state
            out.init()

            # Verify that the record has the same key as was passed to the load method
            out_pk = out.to_pk()
            if out_pk != pk:
                raise RuntimeError(
                    f'Record to_pk() method returns {out_pk} which does '
                    f'not match the argument {pk} passed to the load method'
                )

    def save_many(
        self, records: Iterable[Record], data_set: str
    ) -> None:
        """
        Save many records to the specified dataset, bypassing the commit
        queue and using save options if provided (see SaveOptions
        class for details).

        This method does not implicitly call commit(). The commit queue
        will remain in its original state after the method exits.
        """

        # Iterate over records
        for record in records:
            # Call init to update and validate object state
            record.init()

            # Get primary key and data from record.
            pk = record.to_pk()
            record_dict = record.to_dict()

            # Make deep copy of dictionary in case the original record is changed
            # while the dictionary is persisted in cache
            record_dict = deepcopy(record_dict)

            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(data_set, {})

            # Insert the record into dataset dictionary
            dataset_cache[pk] = record_dict

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
