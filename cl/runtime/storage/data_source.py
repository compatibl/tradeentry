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
from typing import Iterable, Type, TypeVar, Union

from cl.runtime.decorators.data_class_decorator import data_class
from cl.runtime.decorators.data_field_decorator import data_field
from cl.runtime.storage.class_record import ClassRecord
from cl.runtime.storage.record import Record

TKey = TypeVar('TKey', contravariant=True)
TRecord = TypeVar('TRecord', covariant=True)


@data_class
class DataSource(ClassRecord, ABC):
    """Abstract base class for polymorphic data storage API with a directory attribute.

    A data source can be implemented on top a NoSQL DB, relational DB, key-value store, cloud bucket store,
    in-memory cache, distributed cache, filesystem, and types of storage solutions.

    Final record classes stored in a data source must implement the following methods and properties. Some of them
    may be implemented by mixins or intermediate base classes, including those using dataclass and similar frameworks.

    * context - field or property with type Context that has both getter and setter
    * get_key(self) - instance method returning primary key without type as semicolon-delimited string.
      For example, key=`A;B` for a class with two primary key fields that have values `A` and `B`
    * to_dict(self) - instance method serializing self as dictionary
    * from_dict(self, data_dict) - instance method populating self from dictionary
    * get_common_base() - static method returning the type of the common base class for all classes
      stored in the same database table as this class.

    A slash-delimited string parameter `dir` may be used to set up hierarchical data lookup within the data source.

    - Root directory is designed by `/`
    - Permitted character in directory name follow Linux, with `/` in the beginning but not at the end.
    - Each record is stored in a specific directory.
    - During lookup, records in each directory will shadow records with the same key in its base directories.
    - For example, search order when directory '/A/B' is specified is [`/A/B`, `/A`, `/`]
    """

    data_source_id: str = data_field()
    """Unique data source identifier."""

    read_only: bool = data_field(optional=True)
    """Use this flag to mark the data source as readonly. All write operations will fail with error if set."""

    @staticmethod
    def get_common_base():
        """Type of the common base for all classes stored in the same table as this class."""
        return DataSource

    @staticmethod
    def create_key(data_source_id: str) -> str:
        """Create primary key from arguments in semicolon-delimited string format."""
        return data_source_id

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return str(self.data_source_id)

    @abstractmethod
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
        - Error message if any loaded record is not derived from `base_type`.
        - The order of results is the same as the order of argument keys unless `is_unordered` is set.
        - To avoid saving and then loading the records that are created in memory, any argument key that
          is itself derived from base_type will be returned bypassing the data source query.
          Call `get_key()` on records before passing them as argument to reload instead.

        Args:
            base_type: Loaded records must be derived from `base_type`
            keys: Sequence of string keys or key classes for which records will be loaded.
            data_set: Directory-like attribute used to organize the data.
            is_optional: Return None if the record is not found. Default is to raise an error.
            is_optional_key: Return None if a key is None. Default is to raise an error.
            is_unordered: Do not order result in the order of keys. Default is to order the result.
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
        base_type: Type[TRecord],
        key: Union[str, TKey],
        data_set: str,
        *,
        is_optional: bool = None,
        is_optional_key: bool = None,
    ) -> TRecord:
        """
        Load an instance of class derived from base_type from storage using the specified key.

        - Parameter `base_type` determines the database table where the search is performed.
        - Error message if a loaded record is not derived from `base_type`.
        - To avoid saving and then loading the records that are created in memory, any argument key that
          is itself derived from base_type will be returned bypassing the data source query.
          Call `get_key()` on keys before passing them as argument to avoid this behavior.

        Args:
            base_type: Loaded records must be derived from `base_type`
            key: String keys or key class for which the record will be loaded.
            data_set: Directory-like attribute used to organize the data.
            is_optional: Return None if the record is not found. Default is to raise an error.
            is_optional_key: Return None if a key is None. Default is to raise an error.
        """

        # Pass arguments to load_many(...).
        # Add `is_unordered=True` because there is no need to order the result of length one.
        records = self.load_many(
            base_type, [key], data_set, is_optional=is_optional, is_optional_key=is_optional_key, is_unordered=True
        )

        for record in records:
            # We know there is exactly one element
            return record

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
