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
from fastapi.testclient import TestClient
from cl.runtime.routers.schema import schema_router
from cl.runtime.routers.schema.type_request import TypeRequest
from cl.runtime.routers.schema.type_response_util import TypeResponseUtil
from cl.runtime.testing.regression_guard import RegressionGuard

requests = [{"name": "UiAppState"}, {"name": "UiAppState", "user": "TestUser"}]


def test_method():
    """Test coroutine for /schema/typeV2 route."""

    for request in requests:
        # Run the coroutine wrapper added by the FastAPI decorator and validate the result
        request_obj = TypeRequest(**request)
        result_dict = TypeResponseUtil.get_type(request_obj)
        RegressionGuard().write(result_dict)
    RegressionGuard.verify_all()


def test_api():
    """Test REST API for /schema/typeV2 route."""

    test_app = FastAPI()
    test_app.include_router(schema_router.router, prefix="/schema", tags=["Schema"])
    with TestClient(test_app) as test_client:
        for request in requests:
            # Split request headers and query
            request_headers = {"user": request.get("user")}
            request_params = {"name": request.get("name"), "module": request.get("module")}

            # Eliminate empty keys
            request_headers = {k: v for k, v in request_headers.items() if v is not None}
            request_params = {k: v for k, v in request_params.items() if v is not None}

            # Get response
            response = test_client.get("/schema/typeV2", headers=request_headers, params=request_params)
            assert response.status_code == 200
            result = response.json()
            RegressionGuard().write(result)
        RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
