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

from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.routers.user_request import UserRequest
from pydantic import BaseModel
from typing import List


class DatasetResponse(BaseModel):
    """Response data type for the /storage/get_datasets route."""

    name: str | None
    """Name of the dataset."""

    parent: str | None = None
    """Name of the parent dataset."""

    class Config:
        alias_generator = StringUtil.to_pascal_case
        populate_by_name = True

    @classmethod
    def get_datasets(cls, request: UserRequest) -> List[DatasetResponse]:
        """Implements /storage/get_datasets route."""

        # Default response when running locally without authorization
        result_dict = {
            "name": None,
        }

        return [DatasetResponse(**result_dict)]
