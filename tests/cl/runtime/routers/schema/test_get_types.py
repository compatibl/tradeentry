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
from cl.runtime.routers.schema.types_response_item import TypesResponseItem
from cl.runtime.routers.user_request import UserRequest

requests = [{}, {"user": "TestUser"}]

expected_result = {"Name": "TypeDecl", "Module": "Cl.Runtime.Schema.TypeDecl", "Label": "Type Decl"}


def test_method():
    """Test coroutine for /schema/types route."""

    for request in requests:
        # Run the coroutine wrapper added by the FastAPI decorator and get the result
        request_obj = UserRequest(**request)
        result = TypesResponseItem.get_types(request_obj)

        # Check if the result is a list
        assert isinstance(result, list)

        # Check if each item in the result is a TypesResponseItem instance
        assert all(isinstance(x, TypesResponseItem) for x in result)

        type_decl_item = next(x for x in result if x.name == "TypeDecl")
        assert type_decl_item == TypesResponseItem(**expected_result)


def test_api():
    """Test REST API for /schema/types route."""

    test_app = FastAPI()
    test_app.include_router(schema_router.router, prefix="/schema", tags=["Schema"])
    with TestClient(test_app) as test_client:
        for request in requests:
            response = test_client.get("/schema/types", headers=request)
            assert response.status_code == 200
            result = response.json()

            # Check that the result is a list
            assert isinstance(result, list)

            # Check if each item in the result has valid data to construct TypesResponseItem
            for item in result:
                TypesResponseItem(**item)

            type_decl_item = next(x for x in result if x["Name"] == "TypeDecl")
            assert type_decl_item == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
