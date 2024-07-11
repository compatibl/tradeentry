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
from cl.runtime.context.null_progress import NullProgress
from cl.runtime.context.progress import Progress
from cl.runtime.storage.data_source import DataSource
from cl.runtime.storage.data_source_types import TDataset
from logging import Logger
from logging import getLogger


class Context:
    """Provides logging, data source, dataset, and progress reporting."""

    __slots__ = ("__logger", "__data_source", "__dataset", "__progress")

    __logger: Logger
    __data_source: DataSource
    __dataset: TDataset
    __progress: Progress

    def __init__(
        self,
        *,
        logger: Logger | None = None,
        data_source: DataSource | None = None,
        dataset: TDataset = None,
        progress: Progress | None = None,
    ):
        """Normalize and validate inputs."""

        self.__logger = logger if logger is not None else getLogger(__name__)
        self.__data_source = data_source if data_source is not None else DataSource.default()
        self.__dataset = dataset
        self.__progress = progress if progress is not None else NullProgress()

    def logger(self) -> Logger:
        """Return the context logger."""
        return self.__logger

    def data_source(self) -> DataSource | None:
        """Return the context data source or None if not set."""
        if self.__data_source is None:
            raise RuntimeError("Context data source has not been set.")
        return self.__data_source

    def dataset(self) -> TDataset:
        """Return the context dataset or None if not set."""
        return self.__dataset

    def progress(self) -> Progress | None:
        """Return the context progress or None if not set."""
        return self.__progress

    def with_params(
        self,
        *,
        logger: Logger | None = None,
        data_source: DataSource | None = None,
        dataset: TDataset = None,
        progress: Progress | None = None,
    ) -> Context:
        """Create a copy of self where some or all of the attributes are modified."""
        return Context(
            logger=self.__logger if logger is None else logger,
            data_source=self.__data_source if data_source is None else data_source,
            dataset=self.__dataset if dataset is None else dataset,
            progress=self.__progress if progress is None else progress,
        )

    def __enter__(self):
        """Supports `with` operator for resource disposal."""

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Supports `with` operator for resource disposal."""

        # TODO: Support resource disposal for the data source
        if self.__data_source is not None:
            # self.__data_source.disconnect()
            pass

        # Return False to propagate exception to the caller
        return False
