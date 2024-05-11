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

from abc import ABC
from abc import abstractmethod
from cl.runtime.rest.progress import Progress
from cl.runtime.storage.data_source import DataSource
from logging import Logger
from typing import List

from cl.runtime.storage.data_source_types import TDataset


class Context(ABC):
    """Provides logging, data source, dataset, and progress reporting."""

    @staticmethod
    def current() -> Context:
        """Return current context, error message if not set."""
        raise NotImplementedError()

    @abstractmethod
    def logger(self) -> Logger:
        """Return the context logger."""

    @abstractmethod
    def data_source(self) -> DataSource:
        """Return the context data source or None if not set."""

    @abstractmethod
    def read_dataset(self) -> TDataset:
        """Return the context read dataset or None if not set."""

    @abstractmethod
    def write_dataset(self) -> str | None:
        """Return the context write dataset or None if not set."""

    @abstractmethod
    def progress(self) -> Progress:
        """Return the context progress or None if not set."""

    @abstractmethod
    def with_params(
        self,
        *,
        logger: Logger | None = None,
        data_source: DataSource | None = None,
        read_dataset: TDataset = None,
        write_dataset: str | None = None,
        progress: Progress | None = None,
    ) -> Context:
        """Create a copy of self where some or all of the attributes are modified."""

    @abstractmethod
    def __enter__(self):
        """Supports `with` operator for resource disposal."""

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Supports `with` operator for resource disposal."""
