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

from typing import List
from fastapi import APIRouter, Header
from cl.runtime.routers.user_request import UserRequest
from cl.runtime.routers.storage.env_response import EnvResponse

EnvsResponse = List[EnvResponse]

router = APIRouter()


@router.get("/get_envs", response_model=EnvsResponse)  # TODO: Consider changing to /envs for consistency
async def get_envs(
    user: str = Header(None, description="User identifier or identity token"),
) -> EnvsResponse:
    """Information about the environments."""
    return EnvResponse.get_envs(
        UserRequest(
            user=user,
        )
    )
