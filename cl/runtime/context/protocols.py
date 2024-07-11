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

from __future__ import annotations
from typing import Protocol
from cl.runtime.context.progress import Progress
from cl.runtime.storage.data_source import DataSource
from cl.runtime.storage.data_source_types import TDataset
from logging import Logger

from cl.runtime.storage.protocols import DataSourceProtocol


class ProgressProtocol(Protocol):
    """Protocol implemented by objects used for progress reporting."""


class ContextProtocol(Protocol):
    """Protocol implemented by context objects providing logging, data source, dataset, and progress reporting."""

    @classmethod
    def current(cls) -> ContextProtocol:
        """Return current context, error message if not set."""

    def logger(self) -> Logger:
        """Return the logger provided by the context."""

    def data_source(self) -> DataSourceProtocol | None:
        """Return the default data source of the context or None if not set."""

    def dataset(self) -> TDataset:
        """Return the default dataset of the context or None if not set."""

    def progress(self) -> ProgressProtocol | None:
        """Return the progress reporting interface of the context or None if not set."""

    def with_params(
        self,
        *,
        logger: Logger | None = None,
        data_source: DataSource | None = None,
        dataset: TDataset = None,
        progress: Progress | None = None,
    ) -> ContextProtocol:
        """Create a copy of self where some or all of the attributes are modified."""
