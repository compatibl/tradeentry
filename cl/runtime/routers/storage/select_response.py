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

import inflection

from cl.runtime import ClassInfo
from cl.runtime.routers.schema.type_request import TypeRequest
from cl.runtime.routers.schema.type_response_util import TypeResponseUtil
from cl.runtime.routers.storage.select_request import SelectRequest
from pydantic import BaseModel
from pydantic import Field
from typing import Any, Tuple, Type
from typing import Dict
from typing import List

from cl.runtime.storage.data_source_types import TPrimitive

SelectResponseSchema = Dict[str, Any]
SelectResponseData = List[Dict[str, Any]]


def serialize_key(key: Tuple[Type, ...] | TPrimitive) -> str:
    """Serialize key in tuple format."""
    if isinstance(key, tuple):
        # if key[0] is not type:  # TODO: Verify why the check does not work as expected
            # TODO: Check for table type
            # raise RuntimeError(f"First element {key[0]} of {key} is not a type.")
        return ";".join([serialize_key(key_token) for key_token in key[1:]])
    else:
        return key


class SelectResponse(BaseModel):
    """Response data type for the /storage/select route."""

    schema_: SelectResponseSchema = Field(..., alias="schema")
    """Schema field of the response data type for the /storage/select route."""

    data: SelectResponseData
    """Data field of the response data type for the /storage/select route."""

    @staticmethod
    def get_records(request: SelectRequest) -> SelectResponse:
        """Implements /storage/select route."""

        # Default response when running locally without authorization
        type_decl_dict = TypeResponseUtil.get_type(TypeRequest(name=request.type_, module=request.module, user="root"))

        record_module = inflection.underscore(request.module)
        record_class = request.type_
        record_type = ClassInfo.get_class_type(f"{record_module}.{record_class}")

        # TODO: Load from storage instead of creating
        record = record_type()
        keys = [record.get_key()]

        # Convert to semicolon-delimited primary key fields, omitting the first token (table)
        serialized_keys = [serialize_key(key) for key in keys]

        response_dicts = [
            {
                "_t": request.type_,
                "_key": serialized_key,
                "User": "root",  # TODO: Replace hardcoded value
            }
            for serialized_key in serialized_keys
        ]

        return SelectResponse(schema=type_decl_dict, data=response_dicts)
