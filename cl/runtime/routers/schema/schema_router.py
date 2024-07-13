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

from cl.runtime.routers.schema.type_hierarchy_response_item import TypeHierarchyResponseItem
from cl.runtime.routers.schema.type_hierarchy_request import TypeHierarchyRequest
from cl.runtime.routers.schema.type_request import TypeRequest
from cl.runtime.routers.schema.type_response_util import TypeResponseUtil
from cl.runtime.routers.schema.types_response_item import TypesResponseItem
from cl.runtime.routers.user_request import UserRequest
from fastapi import APIRouter
from fastapi import Header
from fastapi import Query
from starlette.requests import Request
from typing import Dict, List

# TODO: Prefix type aliases with T
TypesResponse = List[TypesResponseItem]
TypeResponse = Dict[str, Dict]
TypeHierarchyResponse = List[TypeHierarchyResponseItem]

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


@router.get("/type-hierarchy", response_model=TypeHierarchyResponse)
async def get_type_hierarchy(
    request: Request,
    name: str = Query(..., description="Class name"),  # noqa Suppress report about shadowed built-in type
    return_ancestors: bool = Query(
        False, description="If true, type ancestors will be returned with the specified type."
    ),
) -> TypeHierarchyResponse:
    """Return type class hierarchy."""
    return TypeHierarchyResponseItem.get_types(TypeHierarchyRequest(name=name, return_ancestors=return_ancestors))
