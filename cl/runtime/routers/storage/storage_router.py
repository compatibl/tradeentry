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
from fastapi import APIRouter, Header, Query

from cl.runtime.routers.storage.dataset_response import DatasetResponse
from cl.runtime.routers.storage.datasets_request import DatasetsRequest
from cl.runtime.routers.storage.record_request import RecordRequest
from cl.runtime.routers.storage.record_response import RecordResponse
from cl.runtime.routers.user_request import UserRequest
from cl.runtime.routers.storage.env_response import EnvResponse

EnvsResponse = List[EnvResponse]
DatasetsResponse = List[DatasetResponse]

router = APIRouter()


# TODO: Consider changing to /envs for consistency
@router.get("/get_envs", response_model=EnvsResponse)
async def get_envs(user: str = Header(None, description="User identifier or identity token")) -> EnvsResponse:
    """Information about the environments."""
    return EnvResponse.get_envs(UserRequest(user=user))


# TODO: Consider changing to /datasets for consistency
@router.get("/get_datasets", response_model=DatasetsResponse)
async def get_datasets(
        type: str = Query(..., description="Class name"),  # noqa Suppress report about shadowed built-in type
        module: str = Query(None, description="Dot-delimited module string"),
        user: str = Header(None, description="User identifier or identity token"),
) -> DatasetsResponse:
    """Information about the environments."""
    return DatasetResponse.get_datasets(DatasetsRequest(type_=type, module=module, user=user))


@router.get("/record", response_model=RecordResponse)
async def get_record(
        type: str = Query(..., description="Class name"),  # noqa Suppress report about shadowed built-in type
        key: str = Query(..., description="Primary key fields in semicolon-delimited format"),
        module: str = Query(None, description="Dot-delimited module string"),
        dataset: str = Query(None, description="Dataset string"),
        ignore_record_absence: bool = Query(
            False,
            description="If true, empty response will be returned without error if the record is not found."
        ),
        user: str = Header(None, description="User identifier or identity token"),
) -> RecordResponse:
    """Schema and data for a single record specified by a key."""
    return RecordResponse.get_record(
        RecordRequest(
            type_=type, key=key, module=module, dataset=dataset, ignore_record_absence=ignore_record_absence, user=user
        )
    )
