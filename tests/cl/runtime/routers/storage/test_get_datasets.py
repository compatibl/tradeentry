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
from fastapi import FastAPI

from cl.runtime.routers.storage import storage_router
from cl.runtime.routers.storage.dataset_response import DatasetResponse
from cl.runtime.routers.storage.datasets_request import DatasetsRequest
from fastapi.testclient import TestClient

requests = [{"type": "StubClass"}, {"type": "StubClass", "user": "TestUser"}]

expected_result = [
    {
        "Name": None,
        "Parent": None,
    }
]


def test_method():
    """Test coroutine for /storage/get_envs route."""

    for request in requests:
        # Run the coroutine wrapper added by the FastAPI decorator and get the result
        request_obj = DatasetsRequest(**request)
        result = DatasetResponse.get_datasets(request_obj)

        # Check if the result is a list
        assert isinstance(result, list)

        # Check if each item in the result is a DatasetResponse instance
        assert all(isinstance(x, DatasetResponse) for x in result)

        # Check if each item in the result is a valid DatasetResponse instance
        assert result == [DatasetResponse(**x) for x in expected_result]


def test_api():
    """Test REST API for /storage/get_envs route."""

    test_app = FastAPI()
    test_app.include_router(storage_router.router, prefix="/storage", tags=["Storage"])
    with TestClient(test_app) as test_client:
        for request in requests:
            # Split request headers and query
            request_headers = {"user": request.get("user")}
            request_params = {"type": request.get("type"), "module": request.get("module")}

            # Eliminate empty keys
            request_headers = {k: v for k, v in request_headers.items() if v is not None}
            request_params = {k: v for k, v in request_params.items() if v is not None}

            # Get response
            response = test_client.get("/storage/get_datasets", headers=request_headers, params=request_params)
            assert response.status_code == 200
            result = response.json()

            # Check result
            assert result == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
