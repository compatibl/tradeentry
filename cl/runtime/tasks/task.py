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
from cl.runtime.context.context import Context
from cl.runtime.decorators.handler_decorator import handler
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.tasks.task_queue import TaskQueue
from cl.runtime.tasks.task_queue_key import TaskQueueKey
from cl.runtime.tasks.task_run_key import TaskRunKey
from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class Task(TaskKey, RecordMixin[TaskKey], ABC):
    """
    The task 'execute' method is invoked by the queue to which the task is submitted.

    Notes:
        - The task may be invoked sequentially or in parallel with other tasks
        - The task may be invoked in a different process, thread or machine than the submitting code
          and must be able to acquire the resources required by its 'execute' method in all of these cases
        - The queue creates a new TaskRun record every time the task is submitted
        - The TaskRun record is periodically updated by the queue with the run status
        - The TaskRun record must never be created or modified by the task itself
    """

    parent: TaskKey | None = None
    """Parent task (most actions on the parent or further ancestors will also apply to this task)."""

    def get_key(self) -> TaskKey:
        return TaskKey(task_id=self.task_id)

    @handler
    @abstractmethod
    def execute(self) -> None:
        """Invoked by the queue to which the task is submitted."""

    @handler
    def submit(self, queue: TaskQueueKey) -> TaskRunKey:
        """Submit task to the specified queue."""

        # Get current context
        context = Context.current()

        queue_obj = context.load_one(TaskQueue, queue)  # TODO: Optimize for multiple calls
        task_run_key = queue_obj.submit_task(self)
        return task_run_key
