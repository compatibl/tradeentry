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

from dataclasses import dataclass
from typing import ClassVar

from cl.runtime.context.null_progress import NullProgress
from cl.runtime.context.progress import Progress
from cl.runtime.context.protocols import ProgressProtocol
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.storage.data_source import DataSource
from cl.runtime.storage.data_source_types import TDataset
from logging import Logger

from cl.runtime.storage.protocols import DataSourceProtocol


@dataclass(slots=True, kw_only=True, frozen=True)
class Context:
    """Protocol implemented by context objects providing logging, data source, dataset, and progress reporting."""

    current: ClassVar[Context] = None
    """Return current context, error message if not set."""

    logger: Logger | None = None  # TODO: Specify default logger
    """Return the logger provided by the context."""

    # TODO: Review handling of defaults
    data_source: DataSourceProtocol | None = field(default_factory=lambda: DataSource.default())
    """Return the default data source of the context or None if not set."""

    dataset: TDataset = None
    """Return the default dataset of the context or None if not set."""

    progress: ProgressProtocol = NullProgress()
    """Return the progress reporting interface of the context or None if not set."""

    def __enter__(self):
        """Supports `with` operator for resource disposal."""

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Supports `with` operator for resource disposal."""

        # TODO: Support resource disposal for the data source
        if self.data_source is not None:
            # TODO: Finalize approach to disposal self.data_source.disconnect()
            pass

        # Return False to propagate exception to the caller
        return False
