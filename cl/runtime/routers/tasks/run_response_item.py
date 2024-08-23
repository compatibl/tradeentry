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
from typing import Type, List
from pydantic import BaseModel

from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.routers.tasks.run_error_response_item import RunErrorResponseItem
from cl.runtime.routers.tasks.run_request import RunRequest
from cl.runtime.schema.schema import Schema

from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.tasks.task_runner import TaskRunner
from cl.runtime.tasks.task_status import TaskStatus


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

        # TODO (Roman): request [None] for static handlers explicitly
        # Workaround for static handlers
        requested_keys = request.keys if request.keys else [None]
        key_serializer = StringSerializer()

        type_: Type[RecordProtocol] | type = Schema.get_type_by_short_name(request.table)

        # run task for all keys in request
        for serialized_key in requested_keys:
            key = key_serializer.deserialize_key(serialized_key, type_.get_key_type(None)) \
                if serialized_key is not None else None

            # construct TaskRunner for params from request
            task_runner = TaskRunner(
                record_key=key,
                record_type=type_,
                handler=request.method,
                args=request.arguments_
            )

            try:
                # submit task and convert run_id to string
                run_id_as_str = base64.b64encode(task_runner.submit().task_run_id.bytes).decode()
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
