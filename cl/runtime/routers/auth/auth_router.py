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
from fastapi import APIRouter
from fastapi import Header
from cl.runtime.routers.auth.auth_types_response import AuthTypesResponseItem
from cl.runtime.routers.auth.me_response import MeResponse
from cl.runtime.routers.user_request import UserRequest

AuthTypesResponse = List[AuthTypesResponseItem]
router = APIRouter()


@router.get("/me", response_model=MeResponse)
async def get_me(user: str = Header(None, description="User identifier or identity token")) -> MeResponse:
    """Information about the current user."""
    return MeResponse.get_me(UserRequest(user=user))


@router.get("/types", response_model=AuthTypesResponse)
async def get_types(user: str = Header(None, description="Get available authentication types.")) -> AuthTypesResponse:
    """Get available authentication types."""
    return AuthTypesResponseItem.get_types(UserRequest(user=user))
