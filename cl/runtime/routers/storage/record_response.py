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
from pydantic import BaseModel, Field
from cl.runtime.routers.storage.record_request import RecordRequest
from cl.runtime.routers.storage.record_response_data import RecordResponseData
from cl.runtime.routers.storage.record_response_schema import RecordResponseSchema


class RecordResponse(BaseModel):
    """Response data type for the /storage/record route."""

    schema_: RecordResponseSchema = Field(..., alias="schema")
    """Schema field of the response data type for the /storage/record route."""

    data: RecordResponseData
    """Data field of the response data type for the /storage/record route."""

    @staticmethod
    def get_record(request: RecordRequest) -> RecordResponse:
        """Implements /storage/record route."""

        # Default response when running locally without authorization
        result_dict = {
            "schema":
                {
                    "name": "a"
                },
            "data":
                {
                    "name": "b"
                }
        }
        return RecordResponse(**result_dict)

