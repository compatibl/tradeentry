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

import base64
from typing import Any, List
from uuid import UUID

from pydantic import BaseModel

from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.routers.tasks.task_result_request import TaskResultRequest
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.tasks.v1.task_observer import TaskObserver


class TaskResultResponseItem(BaseModel):
    """Data type for a single item in the response list for the /tasks/run/result route."""

    # TODO (Yauheni): fix the result type according to the actual result type
    result: Any
    """Result of the task run."""

    task_run_id: str
    """Task run id."""

    key: str | None
    """Key of the record."""

    class Config:
        alias_generator = StringUtil.to_pascal_case
        populate_by_name = True

    @staticmethod
    def get_task_results(request: TaskResultRequest) -> List[TaskResultResponseItem]:
        response_items = []
        for run_id_as_str in request.task_run_ids:
            # TODO (Roman): optimize using load_many instead of load_one in TaskObserver.get_result()

            # convert string run_id to UUID and create TaskObserver
            run_id = UUID(bytes=base64.b64decode(run_id_as_str.encode()))
            task_observer = TaskObserver(task_run_id=run_id)

            key = task_observer.get_key()
            key_serializer = StringSerializer()
            # get result and key from TaskObserver and create response item
            response_items.append(
                TaskResultResponseItem(
                    result=task_observer.get_result(),
                    task_run_id=run_id_as_str,
                    key=key_serializer.serialize_key(key) if key else None,
                )
            )

        return response_items
