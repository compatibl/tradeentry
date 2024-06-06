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

from cl.runtime.routers.schema.type_request import TypeRequest
from cl.runtime.routers.schema.type_response_util import TypeResponseUtil
from cl.runtime.routers.storage.record_request import RecordRequest
from pydantic import BaseModel
from pydantic import Field
from typing import Any
from typing import Dict

RecordResponseSchema = Dict[str, Any]
RecordResponseData = Dict[str, Any]


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
        type_decl_dict = TypeResponseUtil.get_type(TypeRequest(name=request.type, module=request.module, user="root"))
        data_dict = {
            "_t": request.type,
            "User": "root",
        }

        # type_decl = TypeDecl(**type_decl_dict)
        return RecordResponse(schema=type_decl_dict, data=data_dict)
