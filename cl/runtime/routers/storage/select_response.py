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
from cl.runtime.serialization.dict_data_serializer import DictDataSerializer
from cl.runtime.serialization.string_key_serializer import StringKeySerializer
from cl.runtime.storage.data_source_types import TPrimitive
from pydantic import BaseModel
from pydantic import Field
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type

SelectResponseSchema = Dict[str, Any]
SelectResponseData = List[Dict[str, Any]]


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

        records = [record_type() for i in range(10)]  # TODO: Load from storage instead of creating

        # TODO: Refactor the code below

        # Convert to semicolon-delimited primary key fields, omitting the first token (table)
        data_serializer = DictDataSerializer(pascalize_keys=True)
        key_serializer = StringKeySerializer()
        serialized_keys_and_records = [
            (key_serializer.serialize_key(x), data_serializer.serialize_data(x)) for x in records
        ]

        # Add _t and _key fields
        [
            record.update({"_t": request.type_, "_key": key, "User": "root"})
            for key, record in serialized_keys_and_records
        ]
        [record.pop("_type") for key, record in serialized_keys_and_records]
        serialized_records = tuple(record for key, record in serialized_keys_and_records)

        return SelectResponse(schema=type_decl_dict, data=serialized_records).dict(by_alias=True)
