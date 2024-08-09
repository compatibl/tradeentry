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
from enum import IntEnum

from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.storage.data_source_types import TDataDict
import re


class FlattenedValueType(IntEnum):
    data = 0
    dict = 1
    list = 2


class FlatDictSerializer(DictSerializer):

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
        if hasattr(data, '__slots__'):
            flattened_value_type = FlattenedValueType.data
        elif isinstance(data, dict):
            flattened_value_type = FlattenedValueType.dict
        elif hasattr(data, '__iter__'):
            flattened_value_type = FlattenedValueType.list

        result = super().serialize_data(data)

        if not is_root and flattened_value_type is not None:
            result = self._add_flattened_type(json.dumps(result), flattened_value_type)

        return result

    def deserialize_data(self, data: TDataDict):

        if isinstance(data, dict):
            converted_data = {}
            for k, v in data.items():
                if isinstance(v, str):
                    converted_value, flattened_type = self._remove_flattened_type(v)

                    if flattened_type is not None:
                        converted_value = json.loads(converted_value)
                else:
                    converted_value = v

                converted_data[k] = converted_value
        else:
            converted_data = data

        return super().deserialize_data(converted_data)
