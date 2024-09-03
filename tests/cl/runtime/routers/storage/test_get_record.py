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

import json
import os
import pytest
from cl.runtime.routers.server import app
from cl.runtime.routers.storage.record_request import RecordRequest
from cl.runtime.routers.storage.record_response import RecordResponse
from fastapi.testclient import TestClient

requests = [
    {"type": "StubDataclassRecord", "key": "A0"},
]

expected_result_file_path = os.path.abspath(__file__).replace(".py", ".expected.json")
with open(expected_result_file_path, "r", encoding="utf-8") as file:
    expected_result = json.load(file)


def test_method():
    """Test coroutine for /storage/record route."""

    for request in requests:
        # Run the coroutine wrapper added by the FastAPI decorator and get the result
        request_obj = RecordRequest(**request)
        result = RecordResponse.get_record(request_obj)

        # Check if the result is a RecordResponse instance
        assert isinstance(result, RecordResponse)

        # Check if there are only "schema" and "data"
        assert [x.strip("_") for x in dict(result).keys()] == ["schema", "data"]

        # Check if each item in the result is a valid RecordResponse instance
        assert result == RecordResponse(**expected_result)


def test_api():
    """Test REST API for /storage/record route."""

    with TestClient(app) as client:
        for request in requests:
            # Split request headers and query
            request_headers = {"user": request.get("user")}
            request_params = {"type": request.get("type"), "key": request.get("key"), "dataset": request.get("dataset")}

            # Eliminate empty keys
            request_headers = {k: v for k, v in request_headers.items() if v is not None}
            request_params = {k: v for k, v in request_params.items() if v is not None}

            # Get response
            response = client.get("/storage/record", headers=request_headers, params=request_params)
            assert response.status_code == 200
            result = response.json()

            # Check result
            assert result == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
