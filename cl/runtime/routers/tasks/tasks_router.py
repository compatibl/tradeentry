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

from cl.runtime.routers.tasks.run_error_response_item import RunErrorResponseItem
from cl.runtime.routers.tasks.run_request import RunRequest
from cl.runtime.routers.tasks.run_response_item import RunResponseItem
from cl.runtime.routers.tasks.task_result_request import TaskResultRequest
from cl.runtime.routers.tasks.task_result_response_item import TaskResultResponseItem
from cl.runtime.routers.tasks.task_status_request import TaskStatusRequest
from cl.runtime.routers.tasks.task_status_response_item import TaskStatusResponseItem
from fastapi import APIRouter
from fastapi import Request
from typing import List

router = APIRouter()


@router.post("/run", response_model=List[RunResponseItem | RunErrorResponseItem])
async def tasks_run(request: Request, payload: RunRequest):
    """Receive params for tasks execute."""
    headers = {}
    request_headers = dict(request.headers)
    for key in ("host", "user", "environment", "cutofftime"):
        headers[key] = request_headers.get(key)

    payload.headers = headers

    return RunResponseItem.run_tasks(payload)


@router.post("/run/cancel")
async def tasks_cancel():
    # TODO: Implement this endpoint if needed
    return None


@router.post("/run/cancel_all")
async def tasks_cancel_all():
    # TODO: Implement this endpoint if needed
    return None


@router.post("/run/status", response_model=List[TaskStatusResponseItem])
async def tasks_status(payload: TaskStatusRequest):
    return TaskStatusResponseItem.get_task_statuses(request=payload)


@router.post("/run/result", response_model=List[TaskResultResponseItem])
async def tasks_result(payload: TaskResultRequest):
    return TaskResultResponseItem.get_task_results(request=payload)
