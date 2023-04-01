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
from typing import Iterable, Optional, Union
from cl.runtime.storage.cl_data_source_key import ClDataSourceKey
from cl.runtime.storage.cl_delete_options import ClDeleteOptions
from cl.runtime.storage.cl_load_options import ClLoadOptions
from cl.runtime.storage.cl_record import ClRecord
from cl.runtime.storage.cl_save_options import ClSaveOptions


@dataclass
class ClDataSource(ClDataSourceKey, ABC):
    """Data source is a logical concept similar to database
    that can be implemented for a document DB, relational DB,
    key-value store, or filesystem. On top of the core
    storage layer, it adds directory-like attribute called
    dataset. 

    Data source API provides the ability to:

    (a) store and query datasets;
    (b) store records in a specific dataset; and
    (c) query record across a group of datasets.

    This record is always stored in root dataset.
    """

    read_only: Optional[bool] = None
    """Use this flag to mark data source as readonly. All write operations will fail with error if set."""

    @abstractmethod
    def flush(self) -> None:
        """Flush data to permanent storage without waiting for the data
        to be flushed automatically or on exit."""
        pass

    @abstractmethod
    def load_one(
        self,
        key: Union[str, ClRecord],
        data_set: str,
        load_options: ClLoadOptions = ClLoadOptions.None_,
    ) -> Optional[ClRecord]:
        """Load one record from the specified dataset by typed key, using load
        options if provided (see rt.LoadOptions class for details).

        Invoking load_one method in a loop for many keys will lead to performance
        deterioration; load_many method should be used instead.

        Depending on data source type, this method may perform
        search in parent datasets and/or data sources.
        """

    @abstractmethod
    def save_many(
        self,
        records: Iterable[ClRecord],
        data_set: str,
        save_options: ClSaveOptions = ClSaveOptions.None_
    ) -> None:
        """
        Save many records to the specified dataset, bypassing the commit
        queue and using save options if provided (see rt.SaveOptions
        class for details).

        This method does not implicitly call commit(). The commit queue
        will remain in its original state after the method exits.
        """

    @abstractmethod
    def save_on_commit(
        self,
        record: ClRecord,
        data_set: str,
        save_options: ClSaveOptions = ClSaveOptions.None_
    ) -> None:
        """
        Add the record to the commit queue using save options if provided
        (see rt.SaveOptions class for details).

        The record will not be saved until a call to commit() which
        executes all pending requests in the commit queue. Alternatively,
        rollback() may be used to clear the commit queue without executing
        the pending requests.
        """

    @abstractmethod
    def delete_many(
        self,
        keys: Iterable[ClRecord],
        data_set: str,
        delete_options: ClDeleteOptions = ClDeleteOptions.None_,
    ) -> None:
        """Delete many records in the specified dataset, bypassing
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

    @abstractmethod
    def delete_on_commit(
        self,
        key: ClRecord,
        data_set: str,
        delete_options: ClDeleteOptions = ClDeleteOptions.None_,
    ) -> None:
        """Add to commit queue the command to delete record in the
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

    @abstractmethod
    def commit(self) -> None:
        """
        Execute all pending save and delete requests in the commit queue
        and clear the queue.
        """
        pass

    @abstractmethod
    def rollback(self) -> None:
        """
        Clear the commit queue without executing the pending save and delete
        requests in the queue.
        """
        pass

    @abstractmethod
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

    def save_one(
        self,
        record: ClRecord,
        data_set: str,
        save_options: ClSaveOptions = ClSaveOptions.None_
    ):
        """
        Save one record to the specified dataset, bypassing the commit
        queue and using save options if provided (see rt.SaveOptions
        class for details).

        This method does not implicitly call commit(). The commit queue
        will remain in its original state after the method exits.

        Saving multiple records one by one using save_one method is
        significantly slower than using either save_many method or a series
        of save_on_commit calls, followed by commit().
        """
        self.save_many([record], data_set, save_options)

    def delete_one(
        self,
        key: ClRecord,
        data_set: str,
        delete_options: ClDeleteOptions = ClDeleteOptions.None_,
    ) -> None:
        """Delete record with argument key in the specified dataset
        bypassing the commit queue, using delete options if provided
        (see rt.DeleteOptions class for details). No error is raised
        if the record does not exist.

        This method does not implicitly call commit(). The commit queue
        will remain in its original state after the method exits.

        Deleting multiple records one by one using delete_one(...) method is
        significantly slower than using either delete_many(...) method or a
        series of delete_on_commit(...) calls, followed by commit().

        Depending on data source implementation, this method may
        delete a record or write the delete marker (rt.DeletedRecord)
        to shadow previous versions of the record or records with
        the same key in a parent dataset. This ensures that records
        with the same primary key in dataset and/or data source lookup
        chain do not become visible after this record is deleted.
        To avoid an additional roundtrip to the data store, the delete
        marker may be written even when the record does not exist.
        """
        self.delete_many([key], data_set, delete_options)

    def __enter__(self):
        """Support resource disposal."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support resource disposal."""
        # Return False to propagate exception to the caller
        return False
