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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Union, Type, Optional

from cl.runtime.core.storage.class_data import class_field
from cl.runtime.core.storage.data_source_key import DataSourceKey
from cl.runtime.core.storage.record import Record


@dataclass
class DataSource(DataSourceKey, ABC):
    """
    Data source is a storage API for polymorphic, hierarchical data that
    can be implemented for a NoSQL DB, relational DB, key-value store,
    cloud storage, in-memory cache, distributed cache, or a filesystem.

    On top of the storage layer, the API adds a directory-like attribute
    called the dataset.

    The data source API provides the ability to:

    * Query the list of datasets;
    * Store and query records in a specific dataset; and
    * Query records across multiple datasets using dataset priority order.
    """

    read_only: bool = class_field(optional=True)
    """Use this flag to mark the data source as readonly. All write operations will fail with error if set."""

    @abstractmethod
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

    @abstractmethod
    def save_many(self, records: Iterable[Record], data_set: str) -> None:
        """
        Save many records to the specified dataset, bypassing the commit queue.

        This method does not implicitly call commit(). The commit queue will 
        remain in its original state after the method exits.
        """

    @abstractmethod
    def save_on_commit(self, record: Record, data_set: str) -> None:
        """
        Add the record to the commit queue.

        The record will not be saved until a call to commit() which
        executes all pending requests in the commit queue. Alternatively,
        rollback() may be used to clear the commit queue without executing
        the pending requests.
        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def commit(self) -> None:
        """
        Execute all pending save and delete requests in the commit queue
        and clear the queue. This will also flush all pending deletes and
        writes in the database driver if applicable.
        """

    @abstractmethod
    def rollback(self) -> None:
        """
        Clear the commit queue without executing the pending save and delete
        requests in the queue.
        """

    @abstractmethod
    def delete_db(self) -> None:
        """
        Permanently delete (drop) the database with all records
        in it without the possibility to recover them later.

        This method should only be used to free storage. For
        all other purposes, methods that preserve history should
        be used.

        ATTENTION - WHEN AVAILABLE, THIS METHOD WILL DELETE ALL DATA
        WITHOUT THE POSSIBILITY OF RECOVERY. USE WITH CAUTION. NOT
        AVAILABLE FOR ALL DATA SOURCE TYPES.

        MUST *NOT* BE IMPLEMENTED IN PRODUCTION DATA SOURCE CODE.
        """

    def load_one(
        self,
        key: Union[str, Record],
        data_set: str,
        *,
        optional_record: bool = False,
        optional_key: bool = False,
        out: Record
    ) -> None:
        """
        Populate the object specified via the 'out' argument with data
        loaded from the specified dataset and key. If the 'key' argument is
        a full record, only its  key will be used.

        Invoking load_one method in a loop for many keys will lead to performance
        deterioration; load_many method should be used instead.
        """

        # Pass arguments to load_many(...)
        self.load_many([key], data_set, optional_record=optional_record, optional_key=optional_key, out=[out])

    def save_one(self, record: Record, data_set: str):
        """
        Save one record to the specified dataset, bypassing the commit queue.

        This method does not implicitly call commit(). The commit queue
        will remain in its original state after the method exits.

        Saving multiple records one by one using save_one method is
        significantly slower than using either save_many method or a series
        of save_on_commit calls, followed by commit().
        """

        # Pass arguments to save_many(...)
        self.save_many([record], data_set)

    def delete_one(self, key: Record, data_set: str) -> None:
        """
        Delete record with argument key in the specified dataset
        bypassing the commit queue. No error is raised if the record
        does not exist. If the 'key' argument is a full record, only its 
        key will be used.

        This method does not implicitly call commit(). The commit queue
        will remain in its original state after the method exits.

        Deleting multiple records one by one using delete_one(...) method is
        significantly slower than using either delete_many(...) method or a
        series of delete_on_commit(...) calls, followed by commit().

        Depending on data source implementation, this method may
        delete a record or write the delete marker (DeletedRecord)
        to shadow previous versions of the record or records with
        the same key in a parent dataset. This ensures that records
        with the same primary key in dataset and/or data source lookup
        chain do not become visible after this record is deleted.
        To avoid an additional roundtrip to the data store, the delete
        marker may be written even when the record does not exist.
        """

        # Pass arguments to delete_many(...)
        self.delete_many([key], data_set)

    def __enter__(self):
        """Support resource disposal."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support resource disposal."""
        # Return False to propagate exception to the caller
        return False
