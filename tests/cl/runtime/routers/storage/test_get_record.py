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
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.testing.regression_guard import RegressionGuard
from cl.runtime.routers.storage import storage_router
from cl.runtime.routers.storage.record_request import RecordRequest
from cl.runtime.routers.storage.record_response import RecordResponse
from stubs.cl.runtime import StubDataclassRecord


def test_method():
    """Test coroutine for /storage/record route."""

    with TestingContext() as context:
        # Save test record
        record = StubDataclassRecord(id=__name__)
        context.save_one(record)

        # Run the coroutine wrapper added by the FastAPI decorator and get the result
        request_obj = RecordRequest(type="StubDataclassRecord", key=record.id)
        result = RecordResponse.get_record(request_obj)

        # Check if the result is a RecordResponse instance
        assert isinstance(result, RecordResponse)

        # Check if there are only "schema" and "data"
        assert [x.strip("_") for x in dict(result).keys()] == ["schema", "data"]

        # Check result
        guard = RegressionGuard()
        guard.write(result)
        guard.verify()


def test_api():
    """Test REST API for /storage/record route."""

    with TestingContext() as context:
        test_app = FastAPI()
        test_app.include_router(storage_router.router, prefix="/storage", tags=["Storage"])
        with TestClient(test_app) as test_client:
            # Save test record
            record = StubDataclassRecord(id=__name__)
            context.save_one(record)

            # Request parameters
            request_obj = RecordRequest(type="StubDataclassRecord", key=record.id)

            # Split request headers and query
            request_headers = {"user": request_obj.user}
            request_params = {"type": request_obj.type, "key": request_obj.key, "dataset": request_obj.dataset}

            # Eliminate empty keys
            request_headers = {k: v for k, v in request_headers.items() if v is not None}
            request_params = {k: v for k, v in request_params.items() if v is not None}

            # Get response
            response = test_client.get("/storage/record", headers=request_headers, params=request_params)
            assert response.status_code == 200
            result = response.json()

            # Check result
            guard = RegressionGuard()
            guard.write(result)
            guard.verify()


if __name__ == "__main__":
    pytest.main([__file__])
