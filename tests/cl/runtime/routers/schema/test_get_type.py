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
from fastapi.testclient import TestClient
from cl.runtime.routers.server import app
from cl.runtime.routers.schema.schema_router import TypeResponse
from cl.runtime.routers.schema.type_response_util import TypeResponseUtil
from cl.runtime.routers.schema.type_request import TypeRequest

requests = [
    {"name": "StubClass"},
    {"name": "StubClass", "user": "TestUser"}
]

expected_result = {'Cl.Runtime.Backend.Core.StubClass': {'Module': {'ModuleName': 'Cl.Runtime.Backend.Core'}, 'Name': 'StubClass', 'Label': 'Ui App State', 'Comment': 'UiAppState.', 'DisplayKind': 'Basic', 'Elements': [{'Key': {'Module': {'ModuleName': 'Cl.Runtime.Backend.Core'}, 'Name': 'User'}, 'Name': 'User', 'Comment': 'A user the app state is applied for.', 'Optional': True}, {'Data': {'Module': {'ModuleName': 'Cl.Runtime.Backend.Core'}, 'Name': 'TabInfo'}, 'Name': 'OpenedTabs', 'Comment': 'Information about opened tabs.', 'Vector': True, 'Optional': True}, {'Value': {'Type': 'Int'}, 'Name': 'ActiveTabIndex', 'Comment': 'Index of active opened tab.', 'Optional': True}, {'Value': {'Type': 'Dict'}, 'Name': 'Versions', 'Comment': 'Component versions.', 'Optional': True}, {'Value': {'Type': 'String'}, 'Name': 'BackendVersion', 'Comment': 'DEPRECATED. Use versions instead.', 'Optional': True}, {'Value': {'Type': 'String'}, 'Name': 'ApplicationName', 'Comment': 'Application name.', 'Optional': True}, {'Value': {'Type': 'Bool'}, 'Name': 'ReadOnly', 'Comment': 'Flag indicating that UI is read-only.', 'Optional': True}, {'Enum': {'Module': {'ModuleName': 'Cl.Runtime.Backend.Core'}, 'Name': 'AppTheme'}, 'Name': 'ApplicationTheme', 'Comment': 'Application theme (dark, light, etc.).', 'Optional': True}], 'Keys': ['User'], 'Implement': {'Handlers': []}}, 'Cl.Runtime.Backend.Core.User': {'Module': {'ModuleName': 'Cl.Runtime.Backend.Core'}, 'Name': 'User', 'Label': 'User', 'Comment': 'User which is allowed to log in.', 'DisplayKind': 'Basic', 'Elements': [{'Value': {'Type': 'String'}, 'Name': 'Username'}, {'Value': {'Type': 'String'}, 'Name': 'FirstName', 'Comment': 'First name of the user.'}, {'Value': {'Type': 'String'}, 'Name': 'LastName', 'Comment': 'Last name of the user.'}, {'Value': {'Type': 'String'}, 'Name': 'Email', 'Comment': 'Email of the user.', 'Optional': True}], 'Keys': ['Username'], 'Implement': {'Handlers': []}}, 'Cl.Runtime.Backend.Core.TabInfo': {'Module': {'ModuleName': 'Cl.Runtime.Backend.Core'}, 'Name': 'TabInfo', 'Label': 'Tab Info', 'Comment': 'Tab info.', 'Kind': 'Element', 'DisplayKind': 'Basic', 'Elements': [{'Data': {'Module': {'ModuleName': 'Cl.Runtime.Backend.Core'}, 'Name': 'BaseTypeInfo'}, 'Name': 'Type', 'Comment': 'Type.'}, {'Value': {'Type': 'Key'}, 'Name': 'Key', 'Comment': 'Key.', 'Optional': True}], 'Keys': None, 'Implement': {'Handlers': []}}, 'Cl.Runtime.Backend.Core.BaseTypeInfo': {'Module': {'ModuleName': 'Cl.Runtime.Backend.Core'}, 'Name': 'BaseTypeInfo', 'Label': 'Base Type Info', 'Comment': 'Base type info.', 'Kind': 'Element', 'DisplayKind': 'Basic', 'Elements': [{'Value': {'Type': 'String'}, 'Name': 'Name', 'Comment': 'Name of type.'}, {'Value': {'Type': 'String'}, 'Name': 'Module', 'Comment': 'Module of type.'}, {'Value': {'Type': 'String'}, 'Name': 'Label', 'Comment': 'Label of type.'}], 'Keys': None, 'Implement': {'Handlers': []}}}


def test_method():
    """Test coroutine for /schema/typeV2 route."""

    for request in requests:

        # Run the coroutine wrapper added by the FastAPI decorator and get the result
        request_obj = TypeRequest(**request)
        result = TypeResponseUtil.get_type(request_obj)

        # Check result
        assert result == expected_result


def test_api():
    """Test REST API for /schema/typeV2 route."""

    with TestClient(app) as client:
        for request in requests:

            # Split request headers and query
            request_headers = {"user": request.get("user")}
            request_params = {"name": request.get("name"), "module": request.get("module")}

            # Eliminate empty keys
            request_headers = {k: v for k, v in request_headers.items() if v is not None}
            request_params = {k: v for k, v in request_params.items() if v is not None}

            # Get response
            response = client.get("/schema/typeV2", headers=request_headers, params=request_params)
            assert response.status_code == 200
            result = response.json()

            # Check result
            assert result == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
