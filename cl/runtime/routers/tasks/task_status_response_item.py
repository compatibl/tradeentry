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
from typing import Dict
from typing import Iterable
from typing import List
from typing import cast
from pydantic import BaseModel
from cl.runtime import Context
from cl.runtime.log.log_entry import LogEntry
from cl.runtime.log.log_entry_level_enum import LogEntryLevelEnum
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.routers.tasks.task_status_request import TaskStatusRequest
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_run_key import TaskRunKey

LEGACY_TASK_STATUS_NAMES_MAP: Dict[str, str] = {
    "PENDING": "Submitted",
    "RUNNING": "Running",
    "PAUSED": "Paused",
    "COMPLETED": "Completed",
    "FAILED": "Failed",
    "CANCELLED": "Cancelled",
}
"""Status name to legacy status name map according to ui convention."""


class TaskStatusResponseItem(BaseModel):
    """Data type for a single item in the response list for the /tasks/run/status route."""

    status_code: str
    """Task status code."""

    task_run_id: str
    """Task run unique id."""

    key: str | None  # TODO: Rename to task_id in REST API for clarity
    """Task key."""

    user_message: str | None
    """Optional user message."""

    class Config:
        alias_generator = CaseUtil.snake_to_pascal_case
        populate_by_name = True

    @classmethod
    def get_task_statuses(cls, request: TaskStatusRequest) -> List[TaskStatusResponseItem]:
        """Get status for tasks in request."""

        # Get current context
        context = Context.current()

        task_run_keys = [TaskRunKey(task_run_id=x) for x in request.task_run_ids]  # TODO: Update if task_run_id is UUID
        task_runs = cast(Iterable[TaskRun], context.load_many(TaskRun, task_run_keys))

        response_items = []
        for task_run in task_runs:
            task_obj = context.load_one(Task, task_run.task)

            # Displayed to the user in case of UserError
            user_message = (
                log_entry.message
                if (
                    task_run.log_entry is not None
                    and (log_entry := context.load_one(LogEntry, task_run.log_entry, is_record_optional=True))
                    is not None
                    and log_entry.level == LogEntryLevelEnum.USER_ERROR
                )
                else None
            )

            response_items.append(
                TaskStatusResponseItem(
                    status_code=LEGACY_TASK_STATUS_NAMES_MAP.get(task_run.status.name),
                    task_run_id=str(task_run.task_run_id),
                    key=task_obj.key_str if hasattr(task_obj, "key_str") else None,
                    user_message=user_message,
                ),
            )

        return response_items
