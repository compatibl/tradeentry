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

from cl.runtime import KeyMixin
from cl.runtime import data_class
from cl.runtime import data_field
from cl.runtime.storage.data_source import DataSource
from cl.runtime.classes.record_mixin import RecordMixin
from typing import Iterable
from typing import Type
from typing import TypeVar
from typing import Union

TKey = TypeVar("TKey", contravariant=True)
TRecord = TypeVar("TRecord", covariant=True)


@data_class
class NullDataSource(DataSource):
    """Null data source discards the data written into it, and returns no data."""

    def load_many(
        self,
        base_type: Type[TRecord],
        keys: Iterable[Union[str, TKey]],
        dataset: str | None = None,
        *,
        is_optional: bool = None,
        is_optional_key: bool = None,
        is_unordered: bool = None,
    ) -> Iterable[TRecord]:
        """Load instances of classes derived from base_type from storage using a sequence of keys."""
        return []

    def save_many(self, records: Iterable[RecordMixin], dataset: str | None = None) -> None:
        """Save many records to the specified dataset, bypassing the commit queue."""
        pass

    def save_on_commit(self, record: RecordMixin, dataset: str | None = None) -> None:
        """Add the record to the commit queue."""
        pass

    def delete_many(self, keys: Iterable[RecordMixin], dataset: str | None = None) -> None:
        """
        Delete many records in the specified dataset, bypassing
        the commit queue. If an element of the 'keys' argument is
        a full record, only its key will be used.
        """
        pass

    def delete_on_commit(self, key: RecordMixin, dataset: str | None = None) -> None:
        """
        Add to commit queue the command to delete record in the
        specified dataset. No error is raised if the record does not
        exist. If the 'key' argument is a full record, only its
        key will be used.
        """
        pass

    def commit(self) -> None:
        """
        Execute all pending save and delete requests in the commit queue
        and clear the queue. This will also flush all pending deletes and
        writes in the database driver if applicable.
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
        Permanently delete (drop) the database with all records
        in it without the possibility to recover them later.
        """
        pass

    def load_one(
        self,
        base_type: Type[TRecord],
        key: Union[str, TKey],
        dataset: str | None = None,
        *,
        is_optional: bool = None,
        is_optional_key: bool = None,
    ) -> TRecord:
        """Load an instance of class derived from base_type from storage using the specified key."""
        return None
