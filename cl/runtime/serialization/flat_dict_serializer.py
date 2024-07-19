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

import json
from dataclasses import dataclass
from enum import IntEnum

from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.storage.data_source_types import TDataDict
import re
import datetime as dt


class FlattenedValueType(IntEnum):
    data = 0
    dict = 1
    list = 2
    date = 3
    datetime = 4
    time = 5


class FlatDictSerializer(DictSerializer):

    primitive_type_names = ["NoneType", "float", "int", "bool", "bytes", "UUID"]

    @staticmethod
    def _add_flattened_type(flattened_value: str, flattened_type: FlattenedValueType) -> str:
        """Add prefix to flattened_value created from flattened_type."""
        flattened_type_prefix = f'::#{flattened_type.name}#'
        return flattened_type_prefix + flattened_value

    @staticmethod
    def _remove_flattened_type(serialized_str_value: str) -> (str, FlattenedValueType | None):
        """
        Check if value contains flattened type prefix and parse it to tuple of unprefixed value and flattened type.
        If value does not contain flattened type prefix will be returned (serialized_str_value, None).
        """

        # check if value contains flattened type value using regex
        flattened_value_pattern = re.compile('::#(?P<type>.*?)#.*')
        flattened_value_match = flattened_value_pattern.match(serialized_str_value)

        if flattened_value_match:
            # get flattened type name according to pattern
            flattened_type = flattened_value_match.group('type')

            # remove flattened type prefix from value
            flattened_value = serialized_str_value.removeprefix(f'::#{flattened_type}#')

            flattened_type = FlattenedValueType[flattened_type]
            return flattened_value, flattened_type
        else:
            # return unmodified value and flattened type None
            return serialized_str_value, None

    def serialize_data(self, data, is_root: bool = False):

        flattened_value_type: FlattenedValueType | None = None

        if isinstance(data, str):
            return data
        elif hasattr(data, '__slots__'):
            flattened_value_type = FlattenedValueType.data
        elif isinstance(data, dict):
            flattened_value_type = FlattenedValueType.dict
        elif hasattr(data, '__iter__'):
            flattened_value_type = FlattenedValueType.list
        elif data.__class__.__name__ == 'date':
            flattened_value_type = FlattenedValueType.date
        elif data.__class__.__name__ == 'datetime':
            flattened_value_type = FlattenedValueType.datetime
        elif data.__class__.__name__ == 'time':
            flattened_value_type = FlattenedValueType.time

        if not is_root and flattened_value_type is not None:

            if flattened_value_type in [FlattenedValueType.date, FlattenedValueType.datetime, FlattenedValueType.time]:
                result = data.isoformat()
            else:
                # TODO (Roman): refactor to avoid nested data json dumps.
                #  It is enough to do single json dump for the entire object.
                result = json.dumps(super().serialize_data(data))

            result = self._add_flattened_type(result, flattened_value_type)
        else:
            result = super().serialize_data(data)

        return result

    def deserialize_data(self, data: TDataDict):

        # check all str values if it is flattened from some type
        if isinstance(data, str):
            converted_data, flattened_type = self._remove_flattened_type(data)

            if flattened_type is not None:
                if flattened_type == FlattenedValueType.date:
                    converted_data = dt.date.fromisoformat(converted_data)
                elif flattened_type == FlattenedValueType.datetime:
                    converted_data = dt.datetime.fromisoformat(converted_data)
                elif flattened_type == FlattenedValueType.time:
                    converted_data = dt.time.fromisoformat(converted_data)
                else:
                    converted_data = json.loads(converted_data)

            if converted_data.__class__.__name__ in ['str', 'date', 'datetime', 'time']:
                return converted_data
        else:
            converted_data = data

        return super().deserialize_data(converted_data)
