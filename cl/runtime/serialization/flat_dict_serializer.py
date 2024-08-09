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
import json
from dataclasses import dataclass
from enum import IntEnum, Enum
from uuid import UUID

from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.string_value_parser import StringValueCustomType, StringValueParser
from cl.runtime.storage.data_source_types import TDataDict
import re
import datetime as dt


class FlatDictSerializer(DictSerializer):
    """
    Serialization for slot-based classes to flat dict (without nested fields).
    Complex types serialize as a json string.
    """

    primitive_type_names = ["NoneType", "float", "int"]

    def serialize_data(self, data, is_root: bool = False):

        if isinstance(data, str):
            return data

        value_custom_type = StringValueParser.get_custom_type(data)

        if not is_root and value_custom_type is not None:

            if value_custom_type in [
                StringValueCustomType.date, StringValueCustomType.datetime, StringValueCustomType.time
            ]:
                result = data.isoformat()
            elif value_custom_type == StringValueCustomType.bool:
                # TODO (Roman): think about a more efficient way to store bool
                result = '1' if data else '0'
            elif value_custom_type == StringValueCustomType.uuid:
                result = base64.b64encode(data.bytes).decode()
            elif value_custom_type == StringValueCustomType.bytes:
                result = base64.b64encode(data).decode()
            else:
                # TODO (Roman): refactor to avoid nested data json dumps.
                #  It is enough to do single json dump for the entire object.
                result = json.dumps(super().serialize_data(data))

            result = StringValueParser.add_type_prefix(result, value_custom_type)
        else:
            result = super().serialize_data(data)

        return result

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
                    converted_data = True if converted_data == '1' else False
                elif custom_type == StringValueCustomType.uuid:
                    converted_data = UUID(bytes=base64.b64decode(converted_data.encode()))
                elif custom_type == StringValueCustomType.bytes:
                    converted_data = base64.b64decode(converted_data.encode())
                else:
                    converted_data = json.loads(converted_data)

            # TODO (Roman): consider to add serialize_primitive() method and override it
            # return deserialized primitives to avoid infinity recursion
            if converted_data.__class__.__name__ in ['str', 'date', 'datetime', 'time', 'bool', 'UUID', 'bytes']:
                return converted_data
        else:
            converted_data = data

        return super().deserialize_data(converted_data)
