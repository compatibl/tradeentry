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
import requests
from cl.runtime.routers.data.type_response import TypeResponse


def test_get_types():

    # Get response data
    url = "http://127.0.0.1:8000/data/types"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()

    # Check if the response is a list
    assert isinstance(data, list)

    # Check if each item in the list is a valid TypeResponse instance
    for item in data:
        TypeResponse(**item)


if __name__ == "__main__":
    pytest.main([__file__])
