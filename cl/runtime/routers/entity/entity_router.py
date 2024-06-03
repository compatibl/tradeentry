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

from cl.runtime.routers.entity.list_panels_request import ListPanelsRequest
from cl.runtime.routers.entity.list_panels_response_item import ListPanelsResponseItem
from fastapi import APIRouter
from fastapi import Header
from fastapi import Query
from typing import List

ListPanelsResponse = List[ListPanelsResponseItem]

router = APIRouter()


# TODO: Consider changing to /panels for consistency
@router.get("/list_panels", response_model=ListPanelsResponse)
async def get_datasets(
    type: str = Query(..., description="Class name"),  # noqa Suppress report about shadowed built-in type
    key: str = Query(None, description="Primary key fields in semicolon-delimited format"),
    dataset: str = Query(None, description="Dataset string"),
    user: str = Header(None, description="User identifier or identity token"),
) -> ListPanelsResponse:
    """List of panels for the specified record."""
    return ListPanelsResponseItem.list_panels(ListPanelsRequest(type=type, key=key, dataset=dataset, user=user))
