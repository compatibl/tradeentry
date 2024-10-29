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

import inspect
from typing import Type, List

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.routers.entity import entity_router
from cl.runtime.routers.entity.list_panels_request import ListPanelsRequest
from cl.runtime.routers.entity.list_panels_response_item import ListPanelsResponseItem
from stubs.cl.runtime import StubDataViewers


def _get_viewer_names_in_pascal_case(record_type: Type) -> List[str]:
    """Get methods with name that starts from 'view_'."""
    result = []
    for name, func in inspect.getmembers(record_type, predicate=inspect.isfunction):
        if name.startswith("view_"):
            name = name.removeprefix("view_")
            name_in_pascal_case = CaseUtil.snake_to_title_case(name)
            result.append(name_in_pascal_case)
    return result


requests = [
    {"type": "StubDataViewers"},
    {"type": "StubDataViewers", "key": "L"},
    {"type": "StubDataViewers", "key": "L", "dataset": "xyz"},
    {"type": "StubDataViewers", "key": "L", "dataset": "xyz", "user": "TestUser"},
]


def test_method():
    """Test coroutine for /entity/list_panels route."""

    for request in requests:
        # Run the coroutine wrapper added by the FastAPI decorator and get the result
        request_obj = ListPanelsRequest(**request)
        result = ListPanelsResponseItem.list_panels(request_obj)

        # Check if the result is a list
        assert isinstance(result, list)

        # Check if each item in the result is a ListPanelsResponseItem instance
        assert all(isinstance(x, ListPanelsResponseItem) for x in result)

        # Check if each item in the result is a valid ListPanelsResponseItem instance
        panel_names_set = set(x.name for x in result)
        expected_panel_names_set = set(_get_viewer_names_in_pascal_case(StubDataViewers))
        assert panel_names_set == expected_panel_names_set


def test_api():
    """Test REST API for /entity/list_panels route."""

    test_app = FastAPI()
    test_app.include_router(entity_router.router, prefix="/entity", tags=["Entity"])
    with TestClient(test_app) as test_client:
        for request in requests:
            # Split request headers and query
            request_headers = {"user": request.get("user")}
            request_params = {"type": request.get("type"), "key": request.get("key"), "dataset": request.get("dataset")}

            # Eliminate empty keys
            request_headers = {k: v for k, v in request_headers.items() if v is not None}
            request_params = {k: v for k, v in request_params.items() if v is not None}

            # Get response
            response = test_client.get("/entity/list_panels", headers=request_headers, params=request_params)
            assert response.status_code == 200
            result = response.json()

            # Check if each item in the result is a valid ListPanelsResponseItem instance
            panel_names_set = set(x["Name"] for x in result)
            expected_panel_names_set = set(_get_viewer_names_in_pascal_case(StubDataViewers))
            assert panel_names_set == expected_panel_names_set


if __name__ == "__main__":
    pytest.main([__file__])
