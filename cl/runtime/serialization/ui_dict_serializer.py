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

from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import List
from typing_extensions import Dict

from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.records.protocols import is_key
from cl.runtime.schema.element_decl import ElementDecl
from cl.runtime.schema.type_decl import TypeDecl
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.dict_serializer import _get_class_hierarchy_slots
from cl.runtime.serialization.dict_serializer import get_type_dict
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.records.protocols import TDataDict


@dataclass(slots=True, kw_only=True)
class UiDictSerializer(DictSerializer):
    """Serialization for slot-based classes to ui format dict (legacy format)."""

    pascalize_keys: bool = True
    """pascalize_keys is True by default."""

    def serialize_data(self, data, select_fields: List[str] | None = None):

        if not self.pascalize_keys:
            raise RuntimeError("Expect ui serialization always with pascalized keys.")

        if data is None:
            return None

        if data.__class__.__name__ in self.primitive_type_names:
            return data
        elif isinstance(data, Enum):
            # serialize enum as its name
            serialized_enum = super(UiDictSerializer, self).serialize_data(data, select_fields)
            pascal_case_value = serialized_enum.get("_name")
            return pascal_case_value
        elif is_key(data):
            # serialize key as string
            key_serializer = StringSerializer()
            return key_serializer.serialize_key(data)
        elif isinstance(data, dict):
            # serialize dict as list of dicts in format [{"key": [key], "value": [value_as_legacy_variant]}]
            serialized_dict_items = []
            for k, v in super(UiDictSerializer, self).serialize_data(data).items():
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
            serialized_data = super(UiDictSerializer, self).serialize_data(data, select_fields)

            # replace "_type" with "_t"
            if "_type" in serialized_data:
                serialized_data["_t"] = data.__class__.__name__
                del serialized_data["_type"]

            serialized_data = {k.removesuffix("_"): v for k, v in serialized_data.items()}

            return serialized_data
        else:
            return super(UiDictSerializer, self).serialize_data(data, select_fields)

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

    def apply_ui_conversion(self, data: TDataDict, element_decl: ElementDecl | None = None) -> TDataDict:
        """
        Apply conversion to make ui data serializable. Extract additional info about types from TypeDecl.

        element_decl can be None for data with _t on root. Then, for nested fields will be used element decls from
        specific TypeDecl object.
        """

        if not self.pascalize_keys:
            raise RuntimeError("Expect ui serialization always with pascalized keys.")

        if isinstance(data, dict):
            if (short_name := data.get("_t")) is not None:

                # Check _t and create TypeDecl object
                type_dict = get_type_dict()
                type_ = type_dict.get(short_name)  # noqa
                type_decl = TypeDecl.for_type(type_)

                # Construct name to element decl map
                type_decl_elements = (
                    {
                        # TODO (Roman): remove extra suffix for elements search after introducing field aliases.
                        #   This is currently needed because ElementDecl removes the _ suffix from the field name.
                        f"{element.name}{extra_suffix}": element
                        for element in type_decl.elements
                        for extra_suffix in ("", "_")
                    }
                    if type_decl.elements is not None
                    else {}
                )

                # Create empty result with _type attribute (instead of _t)
                result = {"_type": short_name}
                for field, value in data.items():
                    if field == "_t":
                        continue

                    # Expect pascal case fields
                    CaseUtil.check_pascal_case(field)

                    if (field_decl := type_decl_elements.get(field)) is not None:
                        # Apply ui conversion for values recursively
                        result[field] = self.apply_ui_conversion(value, field_decl)
                    else:
                        # If element decl is not found for field in data raise RuntimeError
                        raise RuntimeError(
                            f'Data conflicts with type declaration. Field "{field}" not found '
                            f'in "{short_name}" type elements.'
                        )

                return result

        elif isinstance(data, str):
            # Apply ui conversions for string values

            if (enum := element_decl.enum) is not None:
                # Get enum type from element decl and convert value to dict supported by DictSerializer
                enum_type_name = enum.name
                return {"_enum": enum_type_name, "_name": CaseUtil.upper_to_pascal_case(data)}

            elif (key := element_decl.key_) is not None:
                # Get key type from element decl
                key_type_name = key.name
                type_dict = get_type_dict()
                key_type = type_dict.get(key_type_name)  # noqa

                # Deserialize key from string
                key_serializer = StringSerializer()
                result = key_serializer.deserialize_key(data, key_type)

                return result

        elif hasattr(data, "__iter__"):
            # Apply ui conversion for each element in iterable
            return [self.apply_ui_conversion(x, element_decl) for x in data]  # noqa

        # Return unchanged data if there is no ui conversion
        return data
