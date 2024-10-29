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
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_queue import TaskQueue
from cl.runtime.tasks.task_status_enum import TaskStatusEnum


@dataclass(slots=True, kw_only=True)
class ProcessQueue(TaskQueue):
    """Execute tasks sequentially within the queue process."""

    def init(self) -> None:
        # Set default queue timeout with no tasks to 10 min
        if self.timeout_sec is None:
            self.timeout_sec = 10

    def start_queue(self) -> None:
        context = Context.current()
        queue_id = self.queue_id

        # Set timeout
        timeout_delta = dt.timedelta(seconds=self.timeout_sec) if self.timeout_sec is not None else None
        timeout_at = DatetimeUtil.now() + timeout_delta if timeout_delta is not None else None

        # Set the counter of while loop cycles with no tasks
        no_task_cycles = 0
        while True:
            # Get pending tasks
            # TODO: Use DB queries with filter by queue field
            all_tasks = context.load_all(Task)
            awaiting_tasks = [
                task for task in all_tasks
                if task.queue.queue_id == queue_id
                and task.status == TaskStatusEnum.AWAITING
            ]
            pending_tasks = [
                task for task in all_tasks
                if task.queue.queue_id == queue_id
                and task.status == TaskStatusEnum.PENDING
            ]

            # Awaiting tasks have priority over pending tasks
            queued_tasks = awaiting_tasks + pending_tasks

            if queued_tasks:
                # Run found tasks sequentially
                for task in queued_tasks:
                    task.run_task()
                # Reset timeout and no task cycles counter
                timeout_at = DatetimeUtil.now() + timeout_delta if timeout_delta is not None else None
                no_task_cycles = 0
            else:
                if timeout_at is not None and DatetimeUtil.now() > timeout_at:
                    break
                else:
                    no_task_cycles = no_task_cycles + 1

            # Pause for 1 sec more for each no_task_cycle up to 10 sec
            sleep_sec = min(round(pow(2, no_task_cycles)), 8)
            time.sleep(sleep_sec)

    def stop_queue(self) -> None:
        raise NotImplementedError()
