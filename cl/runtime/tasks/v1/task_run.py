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
from typing import Dict, Any

from cl.runtime import RecordMixin
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.tasks.task_run_key import TaskRunKey
from cl.runtime.tasks.task_status import TaskStatus


@dataclass(slots=True, kw_only=True)
class TaskRun(TaskRunKey, RecordMixin[TaskRunKey]):
    """Class with information about task run."""

    status: TaskStatus = missing()
    """Status of task run."""

    result: Any = missing()
    """Result of task."""

    key: KeyProtocol | None = missing()

    def get_key(self) -> KeyProtocol:
        return TaskRunKey(id=self.id)
