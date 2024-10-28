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

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from cl.runtime.context.context import Context
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.tasks.task_queue import TaskQueue
from cl.runtime.tasks.task_queue_key import TaskQueueKey
from cl.runtime.tasks.task_run_key import TaskRunKey


@dataclass(slots=True, kw_only=True)
class Task(TaskKey, RecordMixin[TaskKey], ABC):
    """
    The queue specified in the 'queue' field will invoke the 'run_task' method.

    Notes:
        - A task may run sequentially or in parallel with other tasks
        - A task may run in a different process, thread or machine than the submitting code
          and must be able to acquire the required resources to run in all of these scenarios
    """

    queue: TaskQueueKey = missing()
    """The queue that will run the task once it is saved."""

    def get_key(self) -> TaskKey:
        return TaskKey(task_id=self.task_id)

    @abstractmethod
    def run_task(self) -> None:
        """Invoked by the queue to which the task is submitted."""
