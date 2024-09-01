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

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from cl.runtime.context.context import current_or_default_data_source
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.tasks.v1.task_run import TaskRun
from cl.runtime.tasks.v1.task_run_key import TaskRunKey
from cl.runtime.tasks.v1.task_status import TaskStatus


@dataclass
class TaskObserver:
    """Class to observe task by task_run_id."""

    task_run_id: UUID | None = missing()
    """Unique TaskRun id."""

    def get_status(self) -> TaskStatus:
        """Get task status."""
        task_run = self._get_task_run()
        return task_run.status if task_run else TaskStatus.Empty

    def get_result(self) -> Any:
        """Get task result."""
        task_run = self._get_task_run()
        return task_run.result if task_run else None

    def get_key(self) -> KeyProtocol | None:
        """Get task result."""
        task_run = self._get_task_run()
        return task_run.key if task_run else None

    def _get_task_run(self) -> TaskRun | None:
        data_source = current_or_default_data_source()
        return data_source.load_one(TaskRunKey(id=self.task_run_id))
