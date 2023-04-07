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
from typing import Dict, Iterable, Union, Type, Optional

from cl.runtime.core.schema.type.type_util import TypeUtil
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
            query_type: Type[Record],
            keys: Iterable[Union[str, Record]],
            data_set: str,
            *,
            optional_record: bool = False,
            optional_key: bool = False,
    ) -> Iterable[Record]:
        """
        Return objects of query_type and query_type descendants using a
        sequence of keys. The order of results is the same as the order
        of argument keys.

        To avoid querying records that have already been loaded, any argument
        key that is itself derived from query_type will be returned bypassing
        the data source query. Use to_pk() to avoid this behavior.

        Optional parameters:

        * optional_record: If True, return None if the record is not found.
        * optional_key: If True, accept key=None and return None result.
        """

        result = []
        for key in keys:
            if key is None:
                # Handle key=None
                if optional_key:
                    result.append(None)
                    continue
                else:
                    raise RuntimeError("Key=None but 'optional_key' argument is False or None.")
            elif isinstance(key, query_type):
                # Handle full record passed instead of the key
                result.append(key)
                continue
            elif isinstance(key, str):
                pk = key
            elif isinstance(key, Record):
                pk = key.to_pk()
            else:
                raise RuntimeError(f'Key {key} is not a string, Record, or None')

            # Try to retrieve dataset dictionary, insert if it does not yet exist
            dataset_cache = self._cache.setdefault(data_set, {})

            # Retrieve the record using get method that returns None if the key is not found
            record_dict = dataset_cache.get(pk)

            # Check if result is None
            if record_dict is None:
                if optional_record:
                    result.append(None)
                    continue
                else:
                    raise RuntimeError(
                        f"Record is not found for pk={pk} but 'optional_record' argument is False or None."
                    )

            # Create record instance and populate it from dictionary
            # Final type name is the last element of type discriminators list
            type_discriminators = record_dict['_t']
            final_type = TypeUtil.get_type(type_discriminators[-1])
            record = final_type()
            record.from_dict(record_dict)

            # Call init to update and validate object state
            record.init()

            # Verify that the record has the same key as was passed to the load method
            record_pk = record.to_pk()
            if record_pk != pk:
                raise RuntimeError(
                    f'Record to_pk() method returns {record_pk} which does '
                    f'not match the argument {pk} passed to the load method.'
                )

        return result

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

            # Add the list of types from base to derived
            record_dict["_t"] = TypeUtil.get_hierarchical_discriminator(type(record))

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
