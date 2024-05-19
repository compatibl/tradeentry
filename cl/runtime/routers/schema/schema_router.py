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

from typing import List, Dict
from fastapi import APIRouter, Header, Query

from cl.runtime.routers.schema.type_request import TypeRequest
from cl.runtime.routers.schema.type_response_util import TypeResponseUtil
from cl.runtime.routers.user_request import UserRequest
from cl.runtime.routers.schema.types_response_item import TypesResponseItem

TypesResponse = List[TypesResponseItem]
TypeResponse = Dict[str, int]

router = APIRouter()


@router.get("/types", response_model=TypesResponse)
async def get_types(user: str = Header(None, description="User identifier or identity token")) -> TypesResponse:
    """Information about the record types."""
    return TypesResponseItem.get_types(UserRequest(user=user))


@router.get("/typeV2", response_model=TypeResponse)
async def get_type(
        name: str = Query(..., description="Class name"),  # noqa Suppress report about shadowed built-in type
        module: str = Query(None, description="Dot-delimited module string"),
        user: str = Header(None, description="User identifier or identity token"),
) -> TypeResponse:
    """Schema for the specified type and its dependencies."""
    return TypeResponseUtil.get_type(TypeRequest(name=name, module=module, user=user))
