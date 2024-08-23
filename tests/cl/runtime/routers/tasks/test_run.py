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
from fastapi.testclient import TestClient

from cl.runtime.context.context import current_or_default_data_source
from cl.runtime.routers.tasks.run_error_response_item import RunErrorResponseItem
from cl.runtime.routers.tasks.run_request import RunRequest
from cl.runtime.routers.tasks.run_response_item import RunResponseItem
from cl.runtime.routers.server import app
from cl.runtime.serialization.string_serializer import StringSerializer
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers

stub_handlers = StubHandlers()
key_serializer = StringSerializer()
key_str = key_serializer.serialize_key(stub_handlers.get_key())


simple_requests = [
    {
      "data_source": "DEPRECATED",
      "dataset": "",
      "table": "StubHandlers",
      "keys": [
        key_str
      ],
      "method": "InstanceHandler1b"
    },
    {
      "dataset": "",
      "table": "StubHandlers",
      "method": "StaticHandler1a"
    }
]

save_to_db_requests = [
    {
      "data_source": "DEPRECATED",
      "dataset": "",
      "table": "StubHandlers",
      "keys": [
        key_str
      ],
      "method": "HandlerSaveToDb"
    }
]

expected_records_in_db = [
    [StubDataclassRecord(id="saved_from_handler")]
]


def test_method():
    """Test coroutine for /tasks/run route."""

    data_source = current_or_default_data_source()
    try:
        data_source.save_one(stub_handlers)

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

            # clear existing records
            data_source.delete_many(expected_keys)

            request_object = RunRequest(**request)
            RunResponseItem.run_tasks(request_object)

            actual_records = list(data_source.load_many(expected_keys))
            assert actual_records == expected_records

    finally:
        data_source.delete_db()


def test_api():
    """Test REST API for /tasks/run route."""

    data_source = current_or_default_data_source()
    try:
        data_source.save_one(stub_handlers)

        with TestClient(app) as client:
            for request in simple_requests + save_to_db_requests:
                response = client.post("/tasks/run", json=request)
                assert response.status_code == 200
                result = response.json()

                # Check that the result is a list
                assert isinstance(result, list)

                # Check if each item in the result has valid data to construct RunResponseItem
                for item in result:
                    RunResponseItem(**item)
                    assert item.get('TaskRunId') is not None

                    if request.get('keys'):
                        assert item.get('Key') is not None
                        assert item.get('Key') in request['keys']


            for request, expected_records in zip(save_to_db_requests, expected_records_in_db):

                expected_keys = [rec.get_key() for rec in expected_records]

                # clear existing records
                data_source.delete_many(expected_keys)

                client.post("/tasks/run", json=request)

                actual_records = list(data_source.load_many(expected_keys))
                assert actual_records == expected_records
    finally:
        data_source.delete_db()


if __name__ == "__main__":
    pytest.main([__file__])
