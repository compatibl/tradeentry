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

import pytest
from typing import List, Dict
from fastapi import FastAPI
from starlette.testclient import TestClient
from cl.runtime import Context
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.routers.tasks import tasks_router
from cl.runtime.routers.tasks.run_response_item import handler_queue
from cl.runtime.routers.tasks.task_result_request import TaskResultRequest
from cl.runtime.routers.tasks.task_result_response_item import TaskResultResponseItem
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.tasks.instance_method_task import InstanceMethodTask
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_status_enum import TaskStatusEnum
from stubs.cl.runtime import StubHandlers
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_handlers_key import StubHandlersKey


def _create_tasks_and_get_requests() -> List[Dict]:
    """Creates and saves tasks."""

    # Create handler tasks
    queue_key = handler_queue.get_key()
    tasks = [
        InstanceMethodTask.create(
            task_id=f"{i}",
            queue=queue_key,
            record_or_key=StubHandlersKey(stub_id=f"{i}"),
            method_callable=StubHandlers.run_instance_method_1a,
        )
        for i in range(2)
    ]

    # Get handler task key
    key_serializer = StringSerializer()

    # Create task run records
    t = DatetimeUtil.now()
    task_runs = [
        TaskRun(queue=queue_key, task=task, submit_time=t, update_time=t, status=TaskStatusEnum.COMPLETED, result="result")
        for task in tasks
    ]

    # Init task runs
    for task_run in task_runs:
        task_run.init()

    context = Context.current()
    context.save_many(tasks)
    context.save_many(task_runs)

    stub_handlers = StubHandlers()
    key_serializer = StringSerializer()
    key_str = key_serializer.serialize_key(stub_handlers.get_key())

    requests = [
        {
            "task_run_ids": [str(task_run.task_run_id) for task_run in task_runs],
            "db": "DEPRECATED",
            "dataset": "",
        }
    ]
    return requests



def test_method():
    """Test coroutine for /tasks/run/result route."""

    # TODO: Use TestingContext instead
    with TestingContext() as context:
        for request in _create_tasks_and_get_requests():
            request_object = TaskResultRequest(**request)
            result = TaskResultResponseItem.get_task_results(request_object)

            assert isinstance(result, list)

            for result_item in result:
                assert isinstance(result_item, TaskResultResponseItem)
                assert result_item.task_run_id is not None
                assert result_item.task_run_id in request_object.task_run_ids
                assert result_item.result is not None
                assert result_item.key in ["0", "1"]


def test_api():
    """Test REST API for /tasks/run/result route."""

    # TODO: Use TestingContext instead
    with TestingContext() as context:
        test_app = FastAPI()
        test_app.include_router(tasks_router.router, prefix="/tasks", tags=["Tasks"])
        with TestClient(test_app) as test_client:
            for request in _create_tasks_and_get_requests():
                response = test_client.post("/tasks/run/result", json=request)
                assert response.status_code == 200

                result = response.json()
                assert isinstance(result, list)

                for result_item in result:
                    TaskResultResponseItem(**result_item)
                    assert isinstance(result_item, dict)
                    assert result_item.get("TaskRunId") is not None
                    assert result_item.get("TaskRunId") in request["task_run_ids"]
                    assert result_item.get("Result") is not None
                    assert result_item.get("Key") in ["0", "1"]


if __name__ == "__main__":
    pytest.main([__file__])
