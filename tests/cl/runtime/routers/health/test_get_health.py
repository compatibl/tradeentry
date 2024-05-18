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
from cl.runtime.routers.health.health_response import HealthResponse
from cl.runtime.routers.health.health_router import get_health

expected_result = {"status": 200}


def test_coroutine():
    """Test coroutine for /health route."""

    # Run the coroutine wrapper added by the FastAPI decorator and get the result
    result = asyncio.run(get_health())

    # Check if the result is a list
    assert isinstance(result, HealthResponse)

    # Check if each item in the result is a valid HealthResponse instance
    assert result == HealthResponse(**expected_result)


def test_api():
    """Test REST API for /health route."""

    with TestClient(app) as client:

        response = client.get("/health")
        assert response.status_code == 200
        result = response.json()

        # Check result
        assert result == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
