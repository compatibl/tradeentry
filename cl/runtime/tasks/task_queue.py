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
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.tasks.task_queue_key import TaskQueueKey
from cl.runtime.tasks.task_run_key import TaskRunKey


@dataclass(slots=True, kw_only=True)
class TaskQueue(TaskQueueKey, ABC):
    """
    Invokes the 'execute' method of the submitted tasks sequentially or in parallel with other tasks.

    Notes:
        - The task may be invoked in a different process, thread or machine than the submitting code
          and must be able to acquire the resources required by its 'execute' method in all of these cases
        - The queue creates a new TaskRun record every time the task is submitted
        - The TaskRun record is periodically updated by the queue with the run status and result
        - The TaskRun record must never be modified by the task itself
    """

    def get_key(self) -> TaskQueueKey:
        return TaskQueueKey(queue_id=self.queue_id)

    @abstractmethod
    def start_workers(self) -> None:
        """Start queue workers."""

    @abstractmethod
    def stop_workers(self) -> None:
        """Cancel all active runs and stop queue workers."""

    @abstractmethod
    def cancel_all(self) -> None:
        """Cancel all active runs but do not stop queue workers."""

    @abstractmethod
    def pause_all(self) -> None:
        """Do not start new runs and send pause command to the existing runs."""

    @abstractmethod
    def resume_all(self) -> None:
        """Resume starting new runs and send resume command to existing runs."""

    @abstractmethod
    def submit_task(self, task: TaskKey) -> TaskRunKey:
        """Submit task to this queue (all further access to the task run is provided via the returned TaskRunKey)."""
