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

    @staticmethod
    def get_me() -> MeResponse:
        """Implements /auth/me route."""

        # TODO: Consolidate first and last name into a single string full_name

        # Default response when running locally without authorization
        result_dict = {
          "id": "root",
          "username": "root",
          "first_name": "root",
          "last_name": None,
          "email": None,
          "scopes": ["Read", "Write", "Execute", "Developer"]
        }

        return MeResponse(**result_dict)
