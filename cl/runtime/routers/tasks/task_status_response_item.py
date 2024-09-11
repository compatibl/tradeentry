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

from cl.runtime import Context
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.routers.tasks.task_status_request import TaskStatusRequest
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_run_key import TaskRunKey
from pydantic import BaseModel
from typing import Iterable
from typing import List
from typing import cast
from uuid import UUID


class TaskStatusResponseItem(BaseModel):
    """Data type for a single item in the response list for the /tasks/run/status route."""

    status_code: int
    """Task status code."""

    task_run_id: str
    """Task run unique id."""

    key: str | None  # TODO: Rename to task_id in REST API for clarity
    """Task key."""

    class Config:
        alias_generator = StringUtil.to_pascal_case
        populate_by_name = True

    @classmethod
    def get_task_statuses(cls, request: TaskStatusRequest) -> List[TaskStatusResponseItem]:
        """Get status for tasks in request."""

        # Get current context
        context = Context.current()

        task_run_keys = [TaskRunKey(task_run_id=x) for x in request.task_run_ids]  # TODO: Update if task_run_id is UUID
        task_runs = cast(Iterable[TaskRun], context.load_many(TaskRun, task_run_keys))

        response_items = [
            TaskStatusResponseItem(
                status_code=task_run.status,
                task_run_id=str(task_run.task_run_id),
                key=task_run.task.task_id,
            )
            for task_run in task_runs
        ]
        return response_items
