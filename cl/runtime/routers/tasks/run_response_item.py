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
import traceback
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.routers.tasks.run_error_response_item import RunErrorResponseItem
from cl.runtime.routers.tasks.run_request import RunRequest
from cl.runtime.schema.schema import Schema
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.tasks.instance_handler_task import InstanceHandlerTask
from cl.runtime.tasks.process.process_queue import ProcessQueue
from cl.runtime.tasks.task_status import TaskStatus
from pydantic import BaseModel
from typing import List
from typing import Type

# TODO: Make it possible to configure the queue to use
handler_queue = ProcessQueue(queue_id="Handler Queue")


class RunResponseItem(BaseModel):
    """Data type for a single item in the response list for the /tasks/run route."""

    task_run_id: str
    """Task run id."""

    key: str | None = missing()
    """Key of the record."""

    class Config:
        alias_generator = StringUtil.to_pascal_case
        populate_by_name = True

    @staticmethod
    def run_tasks(request: RunRequest) -> List[RunResponseItem | RunErrorResponseItem]:
        response_items = []

        # TODO: Refactor
        # TODO (Roman): request [None] for static handlers explicitly
        # Workaround for static handlers
        requested_keys = request.keys if request.keys else [None]
        key_serializer = StringSerializer()

        type_: Type[RecordProtocol] | type = Schema.get_type_by_short_name(request.table)

        # run task for all keys in request
        for serialized_key in requested_keys:
            # Create handler task
            # TODO: Support class methods and static methods
            # TODO: Add request.arguments_ and type_
            handler_task = InstanceHandlerTask(
                record_short_name=request.table, key_str=serialized_key, method_name=request.method
            )

            # TODO Include other parameters or use GUID
            handler_task.task_id = f"{handler_task.record_short_name}:{handler_task.key_str}:{handler_task.method_name}"
            task_run_key = handler_queue.submit_task(handler_task)

            try:
                # submit task and convert run_id to string
                run_id_as_str = str(task_run_key.task_run_id)
            except Exception as exc:
                # add error response item if failed to submit task. errors in handler execution handle task runner.
                _traceback = traceback.format_exc()
                response_items.append(
                    RunErrorResponseItem(
                        name="HandlerExecutionException",
                        status_code=TaskStatus.Failed,
                        message=str(exc),
                        stack_trace=_traceback,
                    )
                )
            else:
                # add success response item with submitted task_run_id
                response_items.append(RunResponseItem(key=serialized_key, task_run_id=run_id_as_str))

        return response_items
