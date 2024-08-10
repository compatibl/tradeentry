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
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.records.protocols import is_key
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.dict_serializer import _get_class_hierarchy_slots
from cl.runtime.serialization.string_serializer import StringSerializer
from enum import Enum
from typing import Any
from typing import List
from typing_extensions import Dict


class UiDictSerializer(DictSerializer):
    """Serialization for slot-based classes to ui format dict (legacy format)."""

    def serialize_data(self, data, select_fields: List[str] | None = None):
        # TODO (Roman): make serialization format deserializable

        if data is None:
            return None

        if data.__class__.__name__ in self.primitive_type_names:
            return data
        elif isinstance(data, Enum):
            # serialize enum as its name
            serialized_enum = super().serialize_data(data, select_fields)
            return serialized_enum.get("_name")
        elif is_key(data):
            # serialize key as ';' delimited string
            return ";".join((getattr(data, slot) for slot in data.__slots__))
        elif isinstance(data, dict):
            # serialize dict as list of dicts in format [{"key": [key], "value": [value_as_legacy_variant]}]
            serialized_dict_items = []
            for k, v in super().serialize_data(data).items():
                # TODO (Roman): support more value types in dict
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
        elif getattr(data, "__slots__", None) is not None:
            serialized_data = super().serialize_data(data, select_fields)

            # replace "_type" with "_t"
            if "_type" in serialized_data:
                serialized_data["_t"] = data.__class__.__name__
                del serialized_data["_type"]

            return serialized_data
        else:
            return super().serialize_data(data, select_fields)

    def serialize_record_for_table(self, record: RecordProtocol) -> Dict[str, Any]:
        """
        Serialize record to ui table format.
        Contains only fields of supported types, _key and _t will be added based on record.
        """

        key_serializer = StringSerializer()
        all_slots = _get_class_hierarchy_slots(record.__class__)

        # get subset of slots which supported in table format
        table_slots = [
            slot
            for slot in all_slots
            if (slot_v := getattr(record, slot))
            and (
                # TODO (Roman): check other types for table format
                # select fields if it is primitive, key or enum
                slot_v.__class__.__name__ in self.primitive_type_names
                or is_key(slot_v)
                or isinstance(slot_v, Enum)
            )
        ]

        # serialize record to ui format using table_slots
        table_record: Dict[str, Any] = self.serialize_data(record, select_fields=table_slots)

        # replace "_type" with "_t"
        if "_type" in table_record:
            table_record["_t"] = record.__class__.__name__
            del table_record["_type"]

        # add "_key"
        table_record["_key"] = key_serializer.serialize_key(record.get_key())

        return table_record
