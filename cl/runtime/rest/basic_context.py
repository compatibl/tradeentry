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

from logging import Logger
from typing import List
from cl.runtime import DataSource
from cl.runtime.rest.context import Context
from cl.runtime.rest.progress import Progress


class BasicContext(Context):
    """Provides logging, data source, dataset, and progress reporting."""

    __slots__ = ["__logger", "__data_source", "__read_dataset", "__write_dataset", "__progress"]

    __logger: Logger
    __data_source: DataSource
    __read_dataset: List[str] | str | None
    __write_dataset: str | None
    __progress: Progress

    def __init__(
            self,
            *,
            logger: Logger,
            data_source: DataSource,
            read_dataset: List[str] | str | None = None,
            write_dataset: str | None = None,
            progress: Progress,
    ):
        """Normalize and validate inputs."""

        self.__logger = logger  # Specify default
        self.__data_source = data_source # Specify default
        self.__read_dataset = read_dataset
        self.__write_dataset = write_dataset
        self.__progress = progress # Specify default

    def logger(self) -> Logger:
        """Return the context logger."""
        return self.__logger

    def data_source(self) -> DataSource | None:
        """Return the context data source or None if not set."""
        return self.__data_source

    def read_dataset(self) -> List[str] | str | None:
        """Return the context read dataset or None if not set."""
        return self.__read_dataset

    def write_dataset(self) -> str | None:
        """Return the context write dataset or None if not set."""
        return self.__write_dataset

    def progress(self) -> Progress | None:
        """Return the context progress or None if not set."""
        return self.__progress

    def with_params(
            self,
            *,
            logger: Logger | None = None,
            data_source: DataSource | None = None,
            read_dataset: List[str] | str | None = None,
            write_dataset: str | None = None,
            progress: Progress | None = None,
    ) -> Context:
        """Create a copy of self where some or all of the attributes are modified."""
        return BasicContext(
            logger=self.__logger if logger is None else logger,
            data_source=self.__data_source if data_source is None else data_source,
            read_dataset=self.__read_dataset if read_dataset is None else read_dataset,
            write_dataset=self.__write_dataset if write_dataset is None else write_dataset,
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
