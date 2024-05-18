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
import asyncio
from fastapi.testclient import TestClient
from cl.runtime.routers.app import app
from cl.runtime.routers.auth.me_response import MeResponse
from cl.runtime.routers.auth.auth_router import get_me

expected_result = {
    "id": "root",
    "username": "root",
    "first_name": "root",
    "last_name": None,
    "email": None,
    "scopes": ["Read", "Write", "Execute", "Developer"]
}


def test_coroutine():
    """Test coroutine for /auth/me route."""

    # Run the coroutine wrapper added by the FastAPI decorator and get the result
    result = asyncio.run(get_me())

    # Check if the result is a list
    assert isinstance(result, MeResponse)

    # Check if each item in the result is a valid MeResponse instance
    assert result == MeResponse(**expected_result)


def test_api():
    """Test REST API for /auth/me route."""

    with TestClient(app) as client:

        response = client.get("/auth/me")
        assert response.status_code == 200
        result = response.json()

        # Check result
        assert result == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
