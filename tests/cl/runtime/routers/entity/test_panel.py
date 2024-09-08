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
from cl.runtime import Context
from cl.runtime.routers.entity import entity_router
from cl.runtime.routers.entity.panel_request import PanelRequest
from cl.runtime.routers.entity.panel_response_util import PanelResponseUtil
from cl.runtime.serialization.string_serializer import StringSerializer
from fastapi import FastAPI
from fastapi.testclient import TestClient
from stubs.cl.runtime.decorators.stub_viewers import StubViewers

# create stub with viewers
stub_viewers = StubViewers()
key_serializer = StringSerializer()
key_str = key_serializer.serialize_key(stub_viewers.get_key())


requests = [
    {"type": "StubViewers", "panel_id": "Instance Viewer 1A", "key": key_str},
    {"type": "StubViewers", "panel_id": "Instance Viewer 1B", "key": key_str},
    {"type": "StubViewers", "panel_id": "Instance Viewer 1C", "key": key_str},
]

expected_results = [
    {
        "ViewOf": {
            "_t": "Script",
            "Name": None,
            "Language": "Markdown",
            "Body": ["# Viewer with UI element", "### _Script_"],
            "WordWrap": None,
        }
    },
    {"ViewOf": None},
    {"ViewOf": {"StubId": key_str, "_t": "StubViewersKey"}},
]


def test_method():
    """Test coroutine for /entity/panel route."""

    # TODO: Use UnitTestContext instead
    with Context() as context:
        context.data_source.save_one(stub_viewers)

        for request, expected_result in zip(requests, expected_results):
            request_object = PanelRequest(**request)
            result = PanelResponseUtil.get_content(request_object)

            assert isinstance(result, dict)
            assert result == expected_result


def test_api():
    """Test REST API for /entity/panel route."""

    # TODO: Use UnitTestContext instead
    with Context() as context:
        context.data_source.save_one(stub_viewers)

        test_app = FastAPI()
        test_app.include_router(entity_router.router, prefix="/entity", tags=["Entity"])
        with TestClient(test_app) as test_client:
            for request, expected_result in zip(requests, expected_results):
                # Split request headers and query
                request_headers = {"user": request.get("user")}
                request_params = {
                    "type": request.get("type"),
                    "panel_id": request.get("panel_id"),
                    "key": request.get("key"),
                }

                # Eliminate empty keys
                request_headers = {k: v for k, v in request_headers.items() if v is not None}
                request_params = {k: v for k, v in request_params.items() if v is not None}

                # Get response
                response = test_client.get("/entity/panel", headers=request_headers, params=request_params)
                assert response.status_code == 200
                result = response.json()

                # Check result
                assert result == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
