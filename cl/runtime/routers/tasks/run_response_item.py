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
import traceback
from typing import List
from pydantic import BaseModel
from cl.runtime import Context
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.routers.tasks.run_error_response_item import RunErrorResponseItem
from cl.runtime.routers.tasks.run_request import RunRequest
from cl.runtime.schema.schema import Schema
from cl.runtime.tasks.celery.celery_queue import CeleryQueue
from cl.runtime.tasks.instance_method_task import InstanceMethodTask
from cl.runtime.tasks.static_method_task import StaticMethodTask

# TODO: Make it possible to configure the queue to use for handler execution
handler_queue = CeleryQueue(queue_id="Handler Queue")


class RunResponseItem(BaseModel):
    """Data type for a single item in the response list for the /tasks/run route."""

    task_run_id: str
    """Task run id."""

    key: str | None = missing()
    """Key of the record."""

    class Config:
        alias_generator = CaseUtil.snake_to_pascal_case
        populate_by_name = True

    @classmethod
    def run_tasks(cls, request: RunRequest) -> List[RunResponseItem | RunErrorResponseItem]:
        response_items = []

        # TODO: Refactor
        # TODO (Roman): request [None] for static handlers explicitly
        # Workaround for static handlers
        requested_keys = request.keys if request.keys else [None]

        # Run task for all keys in request
        for serialized_key in requested_keys:
            # Create handler task
            # TODO: Add request.arguments_ and type_
            if serialized_key is not None:
                # Key is not None, this is an instance method

                # Get key type based on table in request
                key_type = Schema.get_type_by_short_name(request.table).get_key_type()  # noqa

                key_type_str = f"{key_type.__module__}.{key_type.__name__}"
                method_name_pascal_case = CaseUtil.snake_to_pascal_case(request.method)
                label = f"{key_type.__name__};{serialized_key};{method_name_pascal_case}"
                handler_task = InstanceMethodTask(
                    label=label,
                    queue=handler_queue.get_key(),
                    key_type_str=key_type_str,
                    key_str=serialized_key,
                    method_name=request.method,
                )
            else:
                # Key is None, this is a @classmethod or @staticmethod
                record_type = Schema.get_type_by_short_name(request.table)
                u = f"{record_type.__module__}.{record_type.__name__}"
                method_name_pascal_case = CaseUtil.snake_to_pascal_case(request.method)
                label = f"{record_type.__name__};{method_name_pascal_case}"
                handler_task = StaticMethodTask(
                    label=label,
                    queue=handler_queue.get_key(),
                    type_str=record_type_str,
                    method_name=request.method,
                )

            # Save and submit task
            Context.current().save_one(handler_task)
            handler_queue.submit_task(handler_task)  # TODO: Rely on query instead
            response_items.append(RunResponseItem(key=serialized_key, task_run_id=handler_task.task_id))

        return response_items
