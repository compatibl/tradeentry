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
from cl.runtime.routers.server import app
from cl.runtime.routers.storage.env_response import EnvResponse
from cl.runtime.routers.user_request import UserRequest

requests = [
    {},
    {"user": "TestUser"}
]

expected_result = [
    {
        "name": "Dev;Runtime;V2",
        "parent": "",  # TODO: Check if None is also accepted
    }
]


def test_method():
    """Test coroutine for /storage/get_envs route."""

    for request in requests:

        # Run the coroutine wrapper added by the FastAPI decorator and get the result
        request_obj = UserRequest(**request)
        result = EnvResponse.get_envs(request_obj)

        # Check if the result is a list
        assert isinstance(result, list)

        # Check if each item in the result is a EnvResponse instance
        assert all(isinstance(x, EnvResponse) for x in result)

        # Check if each item in the result is a valid EnvResponse instance
        assert result == [EnvResponse(**x) for x in expected_result]


def test_api():
    """Test REST API for /storage/get_envs route."""

    with TestClient(app) as client:
        for request in requests:

            response = client.get("/storage/get_envs", headers=request)
            assert response.status_code == 200
            result = response.json()

            # Check result
            assert result == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
