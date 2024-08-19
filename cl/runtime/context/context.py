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

from cl.runtime.context.null_progress import NullProgress
from cl.runtime.context.protocols import ProgressProtocol
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.storage.data_source import DataSource
from cl.runtime.storage.data_source_types import TDataset
from cl.runtime.storage.protocols import DataSourceProtocol
from dataclasses import dataclass
from logging import Logger
from typing import ClassVar
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


def current_or_default_dataset() -> TDataset:
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

    dataset: TDataset = field(default_factory=lambda: current_or_default_dataset())
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
