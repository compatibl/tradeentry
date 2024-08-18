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

import dataclasses
import inflection
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.backend.core.ui_app_state import UiAppState
from cl.runtime.backend.core.ui_app_state_key import UiAppStateKey
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.context.context import current_or_default_data_source
from cl.runtime.routers.schema.type_request import TypeRequest
from cl.runtime.routers.schema.type_response_util import TypeResponseUtil
from cl.runtime.routers.storage.record_request import RecordRequest
from cl.runtime.schema.field_decl import primitive_types  # TODO: Move definition to a separate module
from cl.runtime.schema.schema import Schema
from cl.runtime.schema.type_decl import pascalize
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.serialization.ui_dict_serializer import UiDictSerializer
from pydantic import BaseModel
from pydantic import Field
from typing import Any
from typing import Dict
from typing import List

RecordResponseSchema = Dict[str, Any]
RecordResponseData = Dict[str, Any]


def to_record_dict(node):  # TODO: Apply type hints
    """Recursively apply record dictionary conventions to the argument dictionary."""

    node_type = type(node)
    if node_type in primitive_types:
        # Primitive type, serialize as string
        # TODO: Apply custom formatting
        result = str(node)
        return result
    elif node_type is list:
        # TODO: !!! Generally should not skip nodes that have the value of None
        return [to_record_dict(v) for v in node if v is not None]
    elif node_type is tuple:
        # TODO: Support short alias
        # Generic key, remove Key suffix from key type to obtain table name
        table = node[0].__name__.removesuffix("Key")
        result = ";".join([table] + node[1:])
        return result
    elif node_type.__name__.endswith("Key"):
        # Key type, use semicolon-delimited serialization
        # TODO: Do not use a method from dataclasses
        node_dict = dataclasses.asdict(node)
        result = ";".join(node_dict.keys())
        return result
    elif hasattr(node, "get_key"):
        # Data or record
        # TODO: Do not use a method from dataclasses
        node_dict = dataclasses.asdict(node)
        node_dict = {k: getattr(node, k) for k in node_dict.keys()}
        result = {k: to_record_dict(v) for k, v in node_dict.items() if v is not None}
        return result
    else:
        return node


def to_legacy_dict(node: Dict[str, Any] | List[Dict[str, Any]] | str) -> Dict[str, Any] | List[Dict[str, Any]] | str:
    """Recursively apply record dictionary conventions to the argument dictionary."""

    if isinstance(node, dict):
        # Skip nodes that have the value of None
        # Remove suffix _ from field names if present
        result = {pascalize(k.removesuffix("_")): to_legacy_dict(v) for k, v in node.items() if v is not None}
        return result
    elif isinstance(node, list):
        # Skip nodes that have the value of None
        return [to_legacy_dict(v) for v in node if v is not None]
    elif isinstance(node, tuple):
        # TODO: Support short alias
        # Generic key, remove Key suffix from key type to obtain table name
        table = node[0].__name__.removesuffix("Key")
        result = ";".join([table] + node[1:])
        return result
    else:
        return node


class RecordResponse(BaseModel):
    """Response data type for the /storage/record route."""

    schema_: RecordResponseSchema = Field(..., alias="schema")
    """Schema field of the response data type for the /storage/record route."""

    data: RecordResponseData | None
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

        # load record from storage
        data_source = current_or_default_data_source()
        key_serializer = StringSerializer()

        # TODO (Roman): UiAppState record request from FE should have key in proper format where user is embedded key
        if record_type == UiAppState:
            deserialized_key = UiAppStateKey(user=UserKey(username=request.key))
        else:
            deserialized_key = key_serializer.deserialize_key(request.key, record_type.get_key_type(None))

        record = data_source.load_one(deserialized_key)

        # TODO: Optimize speed using dacite or similar library

        ui_serializer = UiDictSerializer(pascalize_keys=True)
        # serialize record to ui format
        record_dict_in_legacy_format = ui_serializer.serialize_data(record)

        # TODO: Update to return record_dict after legacy dict format is removed
        return RecordResponse(schema=type_decl_dict, data=record_dict_in_legacy_format)
