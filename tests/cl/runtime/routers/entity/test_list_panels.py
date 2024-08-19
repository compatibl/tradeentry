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
from cl.runtime.routers.entity.list_panels_request import ListPanelsRequest
from cl.runtime.routers.entity.list_panels_response_item import ListPanelsResponseItem
from cl.runtime.routers.server import app
from fastapi.testclient import TestClient

requests = [
    {"type": "StubViewers"},
    {"type": "StubViewers", "key": "L"},
    {"type": "StubViewers", "key": "L", "dataset": "xyz"},
    {"type": "StubViewers", "key": "L", "dataset": "xyz", "user": "TestUser"},
]
expected_result = [
    {
        "Name": "Instance Viewer 1A"
    },
    {
        "Name": "Instance Viewer 1B"
    },
    {
        "Name": "Instance Viewer 1C"
    },
    {
        "Name": "Instance Viewer 1D"
    },
    {
        "Name": "Instance Viewer 2A"
    },
    {
        "Name": "Instance Viewer 2B"
    },
    {
        "Name": "Instance Viewer 2C"
    },
    {
        "Name": "Instance Viewer 3A"
    },
]


def test_method():
    """Test coroutine for /storage/get_envs route."""

    for request in requests:
        # Run the coroutine wrapper added by the FastAPI decorator and get the result
        request_obj = ListPanelsRequest(**request)
        result = ListPanelsResponseItem.list_panels(request_obj)

        # Check if the result is a list
        assert isinstance(result, list)

        # Check if each item in the result is a ListPanelsResponseItem instance
        assert all(isinstance(x, ListPanelsResponseItem) for x in result)

        # Check if each item in the result is a valid ListPanelsResponseItem instance
        assert result == [ListPanelsResponseItem(**x) for x in expected_result]


def test_api():
    """Test REST API for /storage/get_envs route."""

    with TestClient(app) as client:
        for request in requests:
            # Split request headers and query
            request_headers = {"user": request.get("user")}
            request_params = {"type": request.get("type"), "key": request.get("key"), "dataset": request.get("dataset")}

            # Eliminate empty keys
            request_headers = {k: v for k, v in request_headers.items() if v is not None}
            request_params = {k: v for k, v in request_params.items() if v is not None}

            # Get response
            response = client.get("/entity/list_panels", headers=request_headers, params=request_params)
            assert response.status_code == 200
            result = response.json()

            # Check result
            assert result == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
