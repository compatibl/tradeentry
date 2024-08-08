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
from enum import Enum

from cl.runtime.records.protocols import is_key
from cl.runtime.serialization.dict_serializer import DictSerializer, _get_class_hierarchy_slots


class UiDictSerializer(DictSerializer):

    def serialize_data(self, data):
        # TODO (Roman): make serialization format deserializable

        if data is None:
            return None

        if isinstance(data, Enum):
            serialized_enum = super().serialize_data(data)
            return serialized_enum.get('_name')
        elif is_key(data):
            return ";".join((getattr(data, slot) for slot in data.__slots__))
        elif isinstance(data, dict):
            # serialize dict as list of dicts in format [{"key": [key], "value": [value_as_legacy_variant]}]
            serialized_dict_items = []
            for k, v in super().serialize_data(data).items():
                if isinstance(v, str):
                    value_type = "String"
                elif isinstance(v, int):
                    value_type = "Int"
                elif isinstance(v, float):
                    value_type = "Double"
                else:
                    raise ValueError(f"Value of type {type(v)} is not supported in dict ui serialization. Value: {v}.")

                serialized_dict_items.append({"key": k, "value": {value_type: v}})

            return serialized_dict_items
        else:
            return super().serialize_data(data)
