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
import time
from dataclasses import dataclass

from cl.runtime import Context
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.tasks.task_queue_key import TaskQueueKey
from cl.runtime.tasks.task_run_key import TaskRunKey
from cl.runtime.tasks.task_status import TaskStatus


@dataclass(slots=True, kw_only=True)
class TaskRun(TaskRunKey, RecordMixin[TaskRunKey]):
    """
    The queue creates this record every time a task is submitted.

    Notes:
        - This record is periodically updated by the queue with the run status and result
        - This record must never be modified by the task itself
    """

    queue: TaskQueueKey = missing()
    """The queue where the task has been submitted."""

    task: TaskKey = missing()
    """The task for which the run is performed."""

    submit_time: dt.datetime = missing()
    """UTC datetime when the task has been submitted for this run."""

    update_time: dt.datetime = missing()
    """UTC datetime of the latest update to this record."""

    status: TaskStatus = missing()
    """Begins from Pending, continues to Running or Paused, and ends with Completed, Failed, or Cancelled."""

    progress: int | None = None
    """Task progress as percent integer from 0 to 100 when available."""

    result: str | None = None
    """Result converted to string."""

    def __post_init__(self):
        # Automatically generate time-ordered unique task run identifier in UUIDv7 format if not yet specified
        if self.task_run_id is None:
            self.task_run_id = str(OrderedUuid.create_one())

    def get_key(self) -> TaskRunKey:
        return TaskRunKey(task_run_id=self.task_run_id)

    @classmethod
    def block_until_completion(cls, task_run_key: TaskRunKey, timeout_sec: int = 10) -> None:
        """Block execution until completion of the specified task run, does not use async/await yet."""

        context = Context.current()
        start_datetime = DatetimeUtil.now()
        while DatetimeUtil.now() < start_datetime + dt.timedelta(seconds=timeout_sec):
            task_run = context.load_one(TaskRun, task_run_key)
            if task_run is not None and task_run.status == TaskStatus.Completed:
                # Test success, task has been completed
                return
            # TODO: Refactor to use queue-specific push communication rather than heartbeat
            time.sleep(1)  # Sleep for 1 second to reduce CPU load

        # Test failure
        raise RuntimeError(f"Task has not been completed after {timeout_sec} sec.")
