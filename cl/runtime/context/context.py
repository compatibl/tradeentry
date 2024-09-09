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

from cl.runtime.records.protocols import KeyProtocol, RecordProtocol
from cl.runtime.context.null_progress import NullProgress
from cl.runtime.context.protocols import ProgressProtocol
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.storage.data_source import DataSource
from cl.runtime.storage.protocols import DataSourceProtocol, TRecord
from dataclasses import dataclass
from logging import Logger
from typing import ClassVar, Iterable, Type
from typing import List

# Use in case progress is not specified
null_progress = NullProgress()


def current_or_default_logger() -> Logger:
    """Return logger of the current context or None if current progress is not set."""
    # TODO: Specify default logger
    return context.logger if (context := Context.current()) is not None else None


def current_or_default_data_source() -> DataSourceProtocol:
    """Return data source of the current context or the default data source if current progress is not set."""
    return context.data_source if (context := Context.current()) is not None else DataSource.default()


def current_or_default_dataset() -> str:
    """Return dataset of the current context or None if current progress is not set."""
    return context.dataset if (context := Context.current()) is not None else None


def current_or_default_progress() -> ProgressProtocol:
    """Return progress API of the current context or NullProgress if current progress is not set."""
    return context.progress if (context := Context.current()) is not None else null_progress


@dataclass(slots=True, kw_only=True, frozen=True)
class Context:
    """Protocol implemented by context objects providing logging, data source, dataset, and progress reporting."""

    __context_stack: ClassVar[List["Context"]] = []  # TODO: Set using ContextVars
    """New current context is pushed to the context stack using 'with Context(...)' clause."""

    logger: Logger | None = field(default_factory=lambda: current_or_default_logger())
    """Return the logger provided by the context."""

    data_source: DataSourceProtocol | None = field(default_factory=lambda: current_or_default_data_source())
    """Return the default data source of the context or None if not set."""

    dataset: str = field(default_factory=lambda: current_or_default_dataset())
    """Default dataset of the context, set to None if not specified"""

    progress: ProgressProtocol = field(default_factory=lambda: current_or_default_progress())
    """Progress reporting interface of the context, set to NullProgress if not specified."""

    @classmethod
    def current(cls):
        """Return the current context or None if not set."""
        return cls.__context_stack[-1] if len(cls.__context_stack) > 0 else None

    def __enter__(self):
        """Supports 'with' operator for resource disposal."""

        # Set current context on entering 'with Context(...)' clause
        self.__context_stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Supports 'with' operator for resource disposal."""

        # Restore the previous current context on exiting from 'with Context(...)' clause
        if len(self.__context_stack) > 0:
            current_context = self.__context_stack.pop()
        else:
            raise RuntimeError("Current context must not be cleared inside 'with Context(...)' clause.")

        if current_context is not self:
            raise RuntimeError("Current context must only be modified by 'with Context(...)' clause.")

        # TODO: Support resource disposal for the data source
        if self.data_source is not None:
            # TODO: Finalize approach to disposal self.data_source.disconnect()
            pass

        # Return False to propagate exception to the caller
        return False

    @classmethod
    def load_one(
        cls,
        record_type: Type[TRecord],
        record_or_key: TRecord | KeyProtocol | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> TRecord | None:
        """
        Load a single record using a key (if a record is passed instead of a key, it is returned without DB lookup)

        Args:
            record_type: Record type to load, error if the result does not match this type
            record_or_key: Record (returned without lookup) or key in object, tuple or string format
            dataset: If specified, append to the root dataset of the data source
            identity: Identity token for database access and row-level security
        """
        return Context.current().data_source.load_one(
            record_type,
            record_or_key,
            dataset=dataset,
            identity=identity,
        )

    @classmethod
    def load_many(
        cls,
        record_type: Type[TRecord],
        records_or_keys: Iterable[TRecord | KeyProtocol | tuple | str | None] | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[TRecord | None] | None:
        """
        Load records using a list of keys (if a record is passed instead of a key, it is returned without DB lookup),
        the result must have the same order as 'records_or_keys'.

        Args:
            record_type: Record type to load, error if the result does not match this type
            records_or_keys: Records (returned without lookup) or keys in object, tuple or string format
            dataset: If specified, append to the root dataset of the data source
            identity: Identity token for database access and row-level security
        """
        return Context.current().data_source.load_many(
            record_type,
            records_or_keys,
            dataset=dataset,
            identity=identity,
        )

    @classmethod
    def load_all(
        cls,
        record_type: Type[TRecord],
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> Iterable[TRecord | None] | None:
        """
        Load all records of the specified type and its subtypes (excludes other types in the same DB table).

        Args:
            record_type: Type of the records to load
            dataset: If specified, append to the root dataset of the data source
            identity: Identity token for database access and row-level security
        """
        return Context.current().data_source.load_all(
            record_type,
            dataset=dataset,
            identity=identity,
        )

    @classmethod
    def save_one(
        cls,
        record: RecordProtocol | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        """
        Save records to storage.

        Args:
            record: Record or None.
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token for database access and row-level security
        """
        Context.current().data_source.save_one(
            record,
            dataset=dataset,
            identity=identity,
        )

    @classmethod
    def save_many(
        cls,
        records: Iterable[RecordProtocol],
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        """
        Save records to storage.

        Args:
            records: Iterable of records.
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token for database access and row-level security
        """
        Context.current().data_source.save_many(
            records,
            dataset=dataset,
            identity=identity,
        )

    @classmethod
    def delete_many(
        cls,
        keys: Iterable[KeyProtocol] | None,
        *,
        dataset: str | None = None,
        identity: str | None = None,
    ) -> None:
        """
        Delete records using an iterable of keys.

        Args:
            keys: Iterable of keys.
            dataset: Target dataset as a delimited string, list of levels, or None
            identity: Identity token for database access and row-level security
        """
        Context.current().data_source.delete_many(
            keys,
            dataset=dataset,
            identity=identity,
        )

    @classmethod
    def delete_all(cls) -> None:
        """
        Permanently delete (drop) all records and schema without the possibility of recovery.
        Error if data source identifier does not match the temp_db pattern in settings.
        """
        # TODO(High): Add a check for temp DB name pattern
        Context.current().data_source.delete_all()
