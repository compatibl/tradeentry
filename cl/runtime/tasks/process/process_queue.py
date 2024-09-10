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

import multiprocessing
from cl.runtime import Context
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.records.protocols import is_record
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.tasks.task_queue import TaskQueue
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_run_key import TaskRunKey
from cl.runtime.tasks.task_status import TaskStatus
from dataclasses import dataclass


def execute_task(task_id: str) -> None:
    """Invoke execute method of the specified task."""

    with Context():
        # Load task object
        task_key = TaskKey(task_id=task_id)
        task = Context.load_one(Task, task_key)
        task.execute()


@dataclass(slots=True, kw_only=True)
class ProcessQueue(TaskQueue):
    """Starts a new process for each task, processes are not reused between tasks."""

    # max_workers: int = missing()  # TODO: Implement support for max_workers
    """The maximum number of processes running concurrently."""

    # TODO: @abstractmethod
    def start_workers(self) -> None:
        """Start queue workers."""

    # TODO: @abstractmethod
    def stop_workers(self) -> None:
        """Cancel all active runs and stop queue workers."""

    # TODO: @abstractmethod
    def cancel_all(self) -> None:
        """Cancel all active runs but do not stop queue workers."""

    # TODO: @abstractmethod
    def pause_all(self) -> None:
        """Do not start new runs and send pause command to the existing runs."""

    # TODO: @abstractmethod
    def resume_all(self) -> None:
        """Resume starting new runs and send resume command to existing runs."""

    def submit_task(self, task: TaskKey) -> None:
        """Submit task to this queue (all further access to the run is provided via the returned TaskRunKey)."""

        # Record the task submission time
        submit_time = DatetimeUtil.now()

        # Save task if provided as record rather than key
        if is_record(task):
            Context.save_one(task)

        # Spawn a daemon process that will exit when this process exits
        worker_process = multiprocessing.Process(target=execute_task, args=(task.task_id,))
        worker_process.start()
        worker_process.join()

        # Save task run record
        task_run = TaskRun()
        task_run.queue = self
        task_run.task = task
        task_run.submit_time = submit_time
        task_run.update_time = submit_time
        task_run.status = TaskStatus.Completed  # TODO: Update after the task is actually completed
        Context.save_one(task_run)
