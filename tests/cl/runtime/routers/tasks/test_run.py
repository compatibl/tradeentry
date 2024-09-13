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
from cl.runtime.context.context import Context
from cl.runtime.routers.tasks import tasks_router
from cl.runtime.routers.tasks.run_error_response_item import RunErrorResponseItem
from cl.runtime.routers.tasks.run_request import RunRequest
from cl.runtime.routers.tasks.run_response_item import RunResponseItem
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.tasks.task_run_key import TaskRunKey
from cl.runtime.testing.celery_fixtures import celery_test_queue_fixture
from cl.runtime.testing.celery_fixtures import check_task_run_completion
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cl.runtime.testing.unit_test_context import UnitTestContext
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers

stub_handlers = StubHandlers()
key_serializer = StringSerializer()
key_str = key_serializer.serialize_key(stub_handlers.get_key())

simple_requests = [
    {
        "data_source": "DEPRECATED",  # TODO: Review and remove
        "dataset": "",
        "table": "StubHandlers",
        "keys": [key_str],
        "method": "InstanceHandler1b",
    },
    {
        "dataset": "",
        "table": "StubHandlers",
        "method": "StaticHandler1a",
    },
]

save_to_db_requests = [
    {
        "data_source": "DEPRECATED",  # TODO: Review and remove
        "dataset": "",
        "table": "StubHandlers",
        "keys": [key_str],
        "method": "HandlerSaveToDb",
    }
]

expected_records_in_db = [[StubDataclassRecord(id="saved_from_handler")]]


def test_method(celery_test_queue_fixture):
    """Test coroutine for /tasks/run route."""

    with UnitTestContext() as context:
        context.save_one(stub_handlers)

        for request in simple_requests + save_to_db_requests:
            request_object = RunRequest(**request)
            result = RunResponseItem.run_tasks(request_object)

            assert isinstance(result, list)

            for result_item in result:
                assert isinstance(result_item, (RunResponseItem, RunErrorResponseItem))
                assert result_item.task_run_id is not None

                if request_object.keys:
                    assert result_item.key is not None
                    assert result_item.key in request_object.keys

        for request, expected_records in zip(save_to_db_requests, expected_records_in_db):
            expected_keys = [rec.get_key() for rec in expected_records]

            request_object = RunRequest(**request)
            response_items = RunResponseItem.run_tasks(request_object)
            [
                check_task_run_completion(TaskRunKey(task_run_id=response_item.task_run_id))
                for response_item in response_items
            ]
            actual_records = list(context.load_many(StubDataclassRecord, expected_keys))
            assert actual_records == expected_records


def test_api(celery_test_queue_fixture):
    """Test REST API for /tasks/run route."""

    # TODO: Use UnitTestContext instead
    with UnitTestContext() as context:
        context.save_one(stub_handlers)

        test_app = FastAPI()
        test_app.include_router(tasks_router.router, prefix="/tasks", tags=["Tasks"])
        with TestClient(test_app) as test_client:
            for request in simple_requests + save_to_db_requests:
                response = test_client.post("/tasks/run", json=request)
                assert response.status_code == 200
                result = response.json()

                # Check that the result is a list
                assert isinstance(result, list)

                # Check if each item in the result has valid data to construct RunResponseItem
                for item in result:
                    RunResponseItem(**item)
                    assert item.get("TaskRunId") is not None

                    if request.get("keys"):
                        assert item.get("Key") is not None
                        assert item.get("Key") in request["keys"]

            for request, expected_records in zip(save_to_db_requests, expected_records_in_db):
                expected_keys = [rec.get_key() for rec in expected_records]

                test_client.post("/tasks/run", json=request)
                request_object = RunRequest(**request)
                response_items = RunResponseItem.run_tasks(request_object)
                [
                    check_task_run_completion(TaskRunKey(task_run_id=response_item.task_run_id))
                    for response_item in response_items
                ]
                actual_records = list(context.load_many(StubDataclassRecord, expected_keys))
                assert actual_records == expected_records


if __name__ == "__main__":
    pytest.main([__file__])
