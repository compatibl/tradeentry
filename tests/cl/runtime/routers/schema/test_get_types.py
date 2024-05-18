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
from cl.runtime.routers.schema.schema_router import get_types
from cl.runtime.routers.schema.type_response import TypeResponse


def test_coroutine():

    # Run the coroutine wrapper added by the FastAPI decorator and get the result
    result = asyncio.run(get_types())

    # Check if the result is a list
    assert isinstance(result, list)

    # Check if each item in the result is a TypeResponse instance
    assert all(isinstance(x, TypeResponse) for x in result)


def test_api():

    with TestClient(app) as client:

        response = client.get("/schema/types")
        assert response.status_code == 200
        result = response.json()

        # Check that the result is a list
        assert isinstance(result, list)

        # Check if each item in the result has valid data to construct TypeResponse
        for item in result:
            TypeResponse(**item)

        # TODO: Test individual results


if __name__ == "__main__":
    pytest.main([__file__])
