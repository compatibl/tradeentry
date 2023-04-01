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

import cl.runtime as rt
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, Iterable, Union


@dataclass
class CacheDataSource(rt.DataSource):
    """Data source based on in-memory cache using Python dict."""

    _cache: Dict[str, Dict] = field(default_factory=dict)

    def init(self) -> None:
        """Update and validate object state after loading from DB and before saving to DB."""

        # Create new cache on init
        self._cache = {}

    def load_many(
        self,
        keys: Iterable[Union[str, rt.Record]],
        data_set: str,
        load_options: rt.LoadOptions = rt.LoadOptions.None_,
        *,
        out: Iterable[rt.Record],
    ) -> None:
        """
        Populate the collection of objects specified via the 'out' parameter
        with data loaded from the specified dataset and collection of keys,
        using load options if provided (see rt.LoadOptions class for details).
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
                if load_options & rt.LoadOptions.IgnoreNullKey == rt.LoadOptions.IgnoreNullKey:
                    return None
                else:
                    raise RuntimeError(
                        'Null key is passed to load_one(...) method ' 'but load_options.IgnoreNullKey flag is not set.'
                    )
            elif isinstance(key, str):
                pk = key
            elif isinstance(key, rt.Record):
                pk = key.to_pk()
            else:
                raise RuntimeError('Key {key} is not a string, derived type of Record, or None')

            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(data_set, {})

            # Retrieve the record using get method that returns None if the key is not found
            record_dict = dataset_cache.get(pk)

            # Check if result is None
            if record_dict is None:
                if load_options & rt.LoadOptions.IgnoreNotFound == rt.LoadOptions.IgnoreNotFound:
                    return None
                else:
                    raise RuntimeError(
                        f'Record is not found for pk={pk} but ' 'load_options.IgnoreNotFound flag is not set.'
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
        self, records: Iterable[rt.Record], data_set: str, save_options: rt.SaveOptions = rt.SaveOptions.None_
    ) -> None:
        """
        Save many records to the specified dataset, bypassing the commit
        queue and using save options if provided (see rt.SaveOptions
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

    def save_on_commit(
        self, record: rt.Record, data_set: str, save_options: rt.SaveOptions = rt.SaveOptions.None_
    ) -> None:
        """
        Add the record to the commit queue using save options if provided
        (see rt.SaveOptions class for details).

        The record will not be saved until a call to commit() which
        executes all pending requests in the commit queue. Alternatively,
        rollback() may be used to clear the commit queue without executing
        the pending requests.
        """

    def delete_many(
        self,
        keys: Iterable[rt.Record],
        data_set: str,
        delete_options: rt.DeleteOptions = rt.DeleteOptions.None_,
    ) -> None:
        """
        Delete many records in the specified dataset, bypassing
        the commit queue and using delete options if provided
        (see rt.DeleteOptions class for details).

        This method does not implicitly call commit(). The commit queue
        will remain in its original state after the method exits.

        Depending on data source implementation, this method may
        delete a record or write the delete marker (rt.DeletedRecord)
        to shadow previous versions of the record or records with
        the same key in a parent dataset. This ensures that records
        with the same primary key in dataset and/or data source lookup
        chain do not become visible after this record is deleted.
        """

    def delete_on_commit(
        self,
        key: rt.Record,
        data_set: str,
        delete_options: rt.DeleteOptions = rt.DeleteOptions.None_,
    ) -> None:
        """
        Add to commit queue the command to delete record in the
        specified dataset, using delete options if provided (see
        rt.DeleteOptions class for details). No error is raised
        if the record does not exist.

        The record will not be saved until a call to commit() which
        executes all pending requests in the commit queue. Alternatively,
        rollback() may be used to clear the commit queue without executing
        the pending requests.

        Depending on data source implementation, this method may
        delete a record or write the delete marker (rt.DeletedRecord)
        to shadow previous versions of the record or records with
        the same key in a parent dataset. This ensures that records
        with the same primary key in dataset and/or data source lookup
        chain do not become visible after this record is deleted.
        To avoid an additional roundtrip to the data store, the delete
        marker may be written even when the record does not exist.
        """
        pass

    def commit(self) -> None:
        """
        Execute all pending save and delete requests in the commit queue
        and clear the queue.
        """
        pass

    def rollback(self) -> None:
        """
        Clear the commit queue without executing the pending save and delete
        requests in the queue.
        """
        pass

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
        pass
