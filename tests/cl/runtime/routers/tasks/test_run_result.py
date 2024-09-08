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

import base64
import pytest
from fastapi import FastAPI

from cl.runtime.context.context import Context
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.routers.tasks import tasks_router
from cl.runtime.routers.tasks.run_response_item import handler_queue
from cl.runtime.routers.tasks.task_result_request import TaskResultRequest
from cl.runtime.routers.tasks.task_result_response_item import TaskResultResponseItem
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.tasks.instance_method_task import InstanceMethodTask
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_status import TaskStatus
from starlette.testclient import TestClient
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers
from stubs.cl.runtime.decorators.stub_handlers_key import StubHandlersKey

# Create handler tasks
tasks = [
    InstanceMethodTask.from_key(
        task_id=f"{i}", key=StubHandlersKey(stub_id=f"{i}"), method=StubHandlers.instance_handler_1a
    )
    for i in range(2)
]

# Get handler task key
key_serializer = StringSerializer()
task_keys_str = [key_serializer.serialize_key(task.get_key()) for task in tasks]

# Create task run records
t = DatetimeUtil.now()
queue_key = handler_queue.get_key()
task_runs = [
    TaskRun(queue=queue_key, task=task, submit_time=t, update_time=t, status=TaskStatus.Completed, result=b"result")
    for task in tasks
]

stub_handlers = StubHandlers()
key_serializer = StringSerializer()
key_str = key_serializer.serialize_key(stub_handlers.get_key())

requests = [
    {
        "task_run_ids": [str(task_run.task_run_id) for task_run in task_runs],
        "data_source": "DEPRECATED",
        "dataset": "",
    }
]


def test_method():
    """Test coroutine for /tasks/run/result route."""

    # TODO: Use UnitTestContext instead
    with Context() as context:
        context.data_source.save_many(tasks)
        context.data_source.save_many(task_runs)

        for request in requests:
            request_object = TaskResultRequest(**request)
            result = TaskResultResponseItem.get_task_results(request_object)

            assert isinstance(result, list)

            for result_item in result:
                assert isinstance(result_item, TaskResultResponseItem)
                assert result_item.task_run_id is not None
                assert result_item.task_run_id in request_object.task_run_ids
                assert result_item.result is not None
                assert result_item.key in task_keys_str


def test_api():
    """Test REST API for /tasks/run/result route."""

    # TODO: Use UnitTestContext instead
    with Context() as context:
        context.data_source.save_many(tasks)
        context.data_source.save_many(task_runs)

        test_app = FastAPI()
        test_app.include_router(tasks_router.router, prefix="/tasks", tags=["Tasks"])
        with TestClient(test_app) as test_client:
            for request in requests:
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
                    assert result_item.get("Key") in task_keys_str


if __name__ == "__main__":
    pytest.main([__file__])
