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

import uuid

import pytest
from starlette.testclient import TestClient

from cl.runtime.context.context import current_or_default_data_source
from cl.runtime.routers.tasks.task_status_request import TaskStatusRequest
from cl.runtime.routers.tasks.task_status_response_item import TaskStatusResponseItem
from cl.runtime.routers.server import app
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_status import TaskStatus
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers

stub_handlers = StubHandlers()
key_serializer = StringSerializer()
key_str = key_serializer.serialize_key(stub_handlers.get_key())


task_runs = [
    TaskRun(id=uuid.uuid4(), status=TaskStatus.Submitted, key=stub_handlers.get_key()),
    TaskRun(id=uuid.uuid4(), status=TaskStatus.Failed, key=stub_handlers.get_key()),
    TaskRun(id=uuid.uuid4(), status=TaskStatus.Completed, key=stub_handlers.get_key()),
]
requests = [
    {
        "task_run_ids": [str(task_run.id) for task_run in task_runs],
        "data_source": "DEPRECATED",
        "dataset": "",
    }
]


def test_method():
    """Test coroutine for /tasks/run/status route."""
    data_source = current_or_default_data_source()
    try:
        data_source.save_one(stub_handlers)
        data_source.save_many(task_runs)

        for request in requests:
            request_object = TaskStatusRequest(**request)
            result = TaskStatusResponseItem.get_task_statuses(request_object)

            assert isinstance(result, list)

            for result_item in result:
                assert isinstance(result_item, TaskStatusResponseItem)
                assert result_item.task_run_id is not None
                assert result_item.task_run_id in request_object.task_run_ids
                assert result_item.status_code is not None
                assert result_item.key == key_str
    finally:
        data_source.delete_db()


def test_api():
    """Test REST API for /tasks/run/status route."""
    data_source = current_or_default_data_source()
    try:
        data_source.save_one(stub_handlers)
        data_source.save_many(task_runs)

        with TestClient(app) as client:
            for request in requests:
                response = client.post("/tasks/run/status", json=request)
                assert response.status_code == 200

                result = response.json()
                assert isinstance(result, list)

                for result_item in result:
                    TaskStatusResponseItem(**result_item)
                    assert isinstance(result_item, dict)
                    assert result_item.get("TaskRunId") is not None
                    assert result_item.get("TaskRunId") in request["task_run_ids"]
                    assert result_item.get("StatusCode") is not None
                    assert result_item.get("Key") == key_str
    finally:
        data_source.delete_db()


if __name__ == "__main__":
    pytest.main([__file__])
