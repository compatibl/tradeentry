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

from dataclasses import asdict

import inflection

from cl.runtime import ClassInfo
from cl.runtime.routers.schema.type_request import TypeRequest
from cl.runtime.routers.schema.type_response_util import TypeResponseUtil
from cl.runtime.routers.storage.record_request import RecordRequest
from pydantic import BaseModel
from pydantic import Field
from typing import Any
from typing import Dict

from cl.runtime.schema.schema import Schema
from cl.runtime.schema.type_decl import pascalize

RecordResponseSchema = Dict[str, Any]
RecordResponseData = Dict[str, Any]


def to_record_dict(node: Dict[str, Any] | List[Dict[str, Any]] | str) -> Dict[str, Any] | List[Dict[str, Any]] | str:
    """Recursively apply record dictionary conventions to the argument dictionary."""

    if isinstance(node, dict):
        # Skip nodes that have the value of None
        # Remove suffix _ from field names if present
        result = {pascalize(k.removesuffix("_")): to_record_dict(v) for k, v in node.items() if v is not None}
        return result
    elif isinstance(node, list):
        # Skip nodes that have the value of None
        return [to_record_dict(v) for v in node if v is not None]
    elif isinstance(node, tuple):
        # The first element of key node tuple is type, the remaining elements are primary key fields
        # Remove suffix _ from field names if present
        key_field_names = node[0].get_key_fields()
        key_field_values = [to_record_dict(v) for v in node[1:]]
        return {pascalize(k.removesuffix("_")): v for k, v in zip(key_field_names, key_field_values)}
    else:
        return node


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

        if True:  # TODO: ";" not in request.key:
            # TODO: Use after module is specified
            record_type = Schema.get_type_by_short_name(request.type)
        else:
            key_tokens = request.key.split(";")
            key_module = inflection.underscore(key_tokens[0])
            key_class = key_tokens[1]

            # record_type = Schema.get_type_by_short_name(request.type)
            # TODO: Use after module is specified
            record_type = ClassInfo.get_class_type(f"{key_module}.{key_class}")

        # TODO: Load from storage instead of creating
        record = record_type()

        # Convert to standard dictionary format
        # TODO: Do not use dataclass method
        standard_record_dict = asdict(record)

        # Apply type declaration dictionary conventions
        record_dict = to_record_dict(standard_record_dict)

        # type_decl = TypeDecl(**type_decl_dict)
        return RecordResponse(schema=type_decl_dict, data=record_dict)
