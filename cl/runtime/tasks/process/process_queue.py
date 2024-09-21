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

import datetime as dt
import multiprocessing
from dataclasses import dataclass
from uuid import UUID
from cl.runtime import Context
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.records.protocols import is_record
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.storage.data_source_types import TDataDict
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.tasks.task_queue import TaskQueue
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_run_key import TaskRunKey
from cl.runtime.tasks.task_status_enum import TaskStatusEnum

context_serializer = DictSerializer()
"""Serializer for the context parameter of 'execute_task' method."""


def execute_task(
    task_run_id: str,
    task_id: str,
    queue_id: str,
    context_data: TDataDict,
) -> None:
    """Invoke execute method of the specified task."""

    # Set is_deserialized flag in context data, will be used to skip some of the initialization code
    context_data["is_deserialized"] = True

    # Deserialize context from 'context_data' parameter to run with the same settings as the caller context
    with context_serializer.deserialize_data(context_data) as context:
        # Get timestamp from task_run_id
        task_run_uuid = UUID(task_run_id)
        submit_time = OrderedUuid.datetime_of(task_run_uuid)

        # Create a task run record in Pending state
        task_run = TaskRun()
        task_run.task_run_id = task_run_id
        task_run.queue = queue_id
        task_run.task = TaskKey(task_id=task_id)
        task_run.submit_time = submit_time
        task_run.update_time = submit_time
        task_run.status = TaskStatusEnum.Pending
        context.save_one(task_run)

        try:
            # Load and execute the task object
            task_key = TaskKey(task_id=task_id)
            task = context.load_one(Task, task_key)
            task.execute()
        except Exception as e:  # noqa
            # Update task run record to report task failure
            task_run.update_time = DatetimeUtil.now()
            task_run.status = TaskStatusEnum.Failed
            task_run.result = str(e)
            context.save_one(task_run)
        else:
            # Update task run record to report task completion
            task_run.update_time = DatetimeUtil.now()
            task_run.status = TaskStatusEnum.Completed
            context.save_one(task_run)


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

    def submit_task(self, task: TaskKey) -> TaskRunKey:
        # Get current context
        context = Context.current()

        # Save task if provided as record rather than key
        if is_record(task):
            context.save_one(task)

        # Create task run identifier and convert to string
        task_run_uuid = OrderedUuid.create_one()
        task_run_id = str(task_run_uuid)
        submit_time = OrderedUuid.datetime_of(task_run_uuid)

        # Save task if provided as record rather than key
        if is_record(task):
            context.save_one(task)

        # Spawn a daemon process that will exit when this process exits
        # TODO: Make asynchronous
        context_data = context_serializer.serialize_data(context)
        worker_process = multiprocessing.Process(
            target=execute_task,
            args=(
                task_run_id,
                task.task_id,
                self.queue_id,
                context_data,
            ),
        )
        worker_process.start()
        worker_process.join()

        # Save task run record
        task_run = TaskRun()
        task_run.queue = self
        task_run.task = task
        task_run.submit_time = submit_time
        task_run.update_time = submit_time
        task_run.status = TaskStatusEnum.Completed  # TODO: Update after the task is actually completed
        context.save_one(task_run)

        return task_run.get_key()
