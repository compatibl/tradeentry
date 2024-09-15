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
from pydantic import Field
from cl.runtime.routers.user_request import UserRequest


class EnvResponse(BaseModel):
    """Response data type for the /storage/get_envs route."""

    name: str = Field(..., alias="Name")
    """Name of the environment."""

    parent: str = Field(..., alias="Parent")
    """Name of the parent environment."""

    @classmethod
    def get_envs(cls, request: UserRequest) -> List[EnvResponse]:
        """Implements /storage/get_envs route."""

        # Default response when running locally without authorization
        result_dict = {
            "Name": "Dev;Runtime;V2",
            "Parent": "",  # TODO: Check if None is also accepted
        }

        return [EnvResponse(**result_dict)]
