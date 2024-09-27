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
from pydantic import BaseModel
from cl.runtime.routers.user_request import UserRequest


class HealthResponse(BaseModel):
    """Response data type for the /health route."""

    status: int
    """HTTP status code."""

    @classmethod
    def get_health(cls, request: UserRequest) -> HealthResponse:
        """Implements /health route."""

        # TODO: Replace stub status code

        # Default response when running locally without authorization
        result_dict = {
            "status": 200,
        }

        return HealthResponse(**result_dict)
