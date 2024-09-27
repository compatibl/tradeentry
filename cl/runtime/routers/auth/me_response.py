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

from __future__ import annotations
from typing import List
from pydantic import BaseModel
from cl.runtime.routers.user_request import UserRequest


class MeResponse(BaseModel):
    """Response data type for the /auth/me route."""

    id: str
    """Class name (may be customized in settings)."""

    username: str
    """Module path in dot-delimited format (may be customized in settings)."""

    first_name: str
    """Type label displayed in the UI is humanized class name (may be customized in settings)."""

    last_name: str | None
    """Class name (may be customized in settings)."""

    email: str | None
    """Module path in dot-delimited format (may be customized in settings)."""

    scopes: List[str] | None
    """Type label displayed in the UI is humanized class name (may be customized in settings)."""

    @classmethod
    def get_me(cls, request: UserRequest) -> MeResponse:
        """Implements /auth/me route."""

        # Get user from the request or use default value if not specified
        # TODO: Obtain default user from settings
        user = "root" if request.user is None else request.user

        # Create response
        # TODO: Consolidate first and last name into a single string full_name
        result_dict = {
            "id": user,
            "username": user,
            "first_name": user,
            "last_name": None,
            "email": None,
            "scopes": ["Read", "Write", "Execute", "Developer"],
        }

        return MeResponse(**result_dict)
