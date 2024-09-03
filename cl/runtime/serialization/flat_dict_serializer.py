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

import base64
import datetime as dt
import json
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.string_value_parser import StringValueCustomType
from cl.runtime.serialization.string_value_parser import StringValueParser
from cl.runtime.storage.data_source_types import TDataDict
from typing import List
from uuid import UUID


class FlatDictSerializer(DictSerializer):
    """
    Serialization for slot-based classes to flat dict (without nested fields).
    Complex types serialize as a json string.
    """

    primitive_type_names = ["NoneType", "float", "int"]

    def serialize_data(self, data, select_fields: List[str] | None = None, *, is_root: bool = False):
        if isinstance(data, str):
            return data

        if data.__class__.__name__ in super().primitive_type_names:
            serialized_data = data
        else:
            serialized_data = super().serialize_data(data, select_fields)

        value_custom_type = StringValueParser.get_custom_type(serialized_data)

        if not is_root and value_custom_type is not None:
            handled_serialized_value = None
            if serialized_data.__class__.__name__ in ("date", "datetime", "time"):
                handled_serialized_value = serialized_data.isoformat()
            elif serialized_data.__class__.__name__ == "bool":
                # TODO (Roman): think about a more efficient way to store bool
                handled_serialized_value = "1" if data else "0"
            elif serialized_data.__class__.__name__ == "UUID":
                handled_serialized_value = str(data)
            elif serialized_data.__class__.__name__ == "bytes":
                handled_serialized_value = base64.b64encode(data).decode()
            elif isinstance(serialized_data, (dict, list)):
                # TODO (Roman): refactor to avoid nested data json dumps.
                #  It is enough to do single json dump for the entire object.
                handled_serialized_value = json.dumps(serialized_data)

            return (
                StringValueParser.add_type_prefix(handled_serialized_value, value_custom_type)
                if handled_serialized_value is not None
                else serialized_data
            )
        else:
            return serialized_data

    def deserialize_data(self, data: TDataDict):
        # check all str values if it is flattened from some type
        if isinstance(data, str):
            converted_data, custom_type = StringValueParser.parse(data)

            if custom_type is not None:
                if custom_type == StringValueCustomType.date:
                    converted_data = dt.date.fromisoformat(converted_data)
                elif custom_type == StringValueCustomType.datetime:
                    converted_data = dt.datetime.fromisoformat(converted_data)
                elif custom_type == StringValueCustomType.time:
                    converted_data = dt.time.fromisoformat(converted_data)
                elif custom_type == StringValueCustomType.bool:
                    converted_data = True if converted_data == "1" else False
                elif custom_type == StringValueCustomType.uuid:
                    converted_data = UUID(converted_data)
                elif custom_type == StringValueCustomType.bytes:
                    converted_data = base64.b64decode(converted_data.encode())
                else:
                    converted_data = json.loads(converted_data)

            # TODO (Roman): consider to add serialize_primitive() method and override it
            # return deserialized primitives to avoid infinity recursion
            if converted_data.__class__.__name__ in super().primitive_type_names:
                return converted_data
        else:
            converted_data = data

        return super().deserialize_data(converted_data)
