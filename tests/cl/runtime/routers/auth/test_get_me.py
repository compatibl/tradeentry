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
from cl.runtime.routers.auth import auth_router
from cl.runtime.routers.auth.me_response import MeResponse
from cl.runtime.routers.auth.me_response import UserRequest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Any
from typing import Dict

requests = [{}, {"user": "TestUser"}]


def get_expected_result(request_obj: UserRequest) -> Dict[str, Any]:
    """Get expected result for the user."""

    # Get user from the request or use default value if not specified
    # TODO: Obtain default user from settings
    user = request_obj.user if request_obj.user is not None else "root"

    return {
        "id": user,
        "username": user,
        "first_name": user,
        "last_name": None,
        "email": None,
        "scopes": ["Read", "Write", "Execute", "Developer"],
    }


def test_method():
    """Test coroutine for /auth/me route."""

    for request in requests:
        # Run the coroutine wrapper added by the FastAPI decorator and get the result
        request_obj = UserRequest(**request)
        result = MeResponse.get_me(request_obj)

        # Check the result
        expected_result = get_expected_result(request_obj)
        assert result == MeResponse(**expected_result)


def test_api():
    """Test REST API for /auth/me route."""

    test_app = FastAPI()
    test_app.include_router(auth_router.router, prefix="/auth", tags=["Authorization"])
    with TestClient(test_app) as test_client:
        for request in requests:
            response = test_client.get("/auth/me", headers=request)
            assert response.status_code == 200
            result = response.json()

            # Check result
            request_obj = UserRequest(**request)
            expected_result = get_expected_result(request_obj)
            assert result == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
