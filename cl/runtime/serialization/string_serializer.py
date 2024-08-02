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
from typing import Any, Type, Dict, List
import datetime as dt

import base64
from uuid import UUID

from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.serialization.string_value_parser import StringValueParser, StringValueCustomType
from cl.runtime.storage.data_source_types import TDataset

# TODO (Roman): remove dependency from dict_serializer
from cl.runtime.serialization.dict_serializer import alias_dict, type_dict


primitive_type_names = ["NoneType", "str", "float", "int", "bool", "date", "time", "datetime", "bytes", "UUID"]
"""Detect primitive type by checking if class name is in this list."""


# TODO: Add checks for custom override of default serializer inside the class
class StringSerializer:
    """Serialize dataset and key to string, flattening hierarchical structure."""

    def serialize_dataset(self, dataset: TDataset) -> Any:
        """Serialize dataset to backslash-delimited string (empty string for None), flattening composite datasets."""

        if dataset is None:
            return ""
        elif dataset.__class__.__name__ in primitive_type_names:
            if isinstance(dataset, str):
                if dataset.startswith("\\") or dataset.endswith("\\"):
                    raise RuntimeError(f"Dataset or dataset token '{dataset}' must not begin or end with backslash.")
                if dataset.startswith(" ") or dataset.endswith(" "):
                    raise RuntimeError(f"Dataset or dataset token '{dataset}' must not begin or end with whitespace.")
            # TODO: Apply rules depending on the specific primitive type
            return str(dataset)
        elif isinstance(dataset, Enum):
            return dataset.name
        elif getattr(dataset, "__iter__", None) is not None:
            return "\\".join(self.serialize_dataset(token) for token in dataset)
        else:
            raise RuntimeError(f"Invalid dataset or its token {dataset}. Valid token types are None, "
                               f"primitive types, enum or their iterables.")

    def _serialize_key_token(self, data) -> str:

        if data is None:
            # TODO (Roman): make different None and empty string
            return ""

        if isinstance(data, str):
            return data

        value_custom_type = StringValueParser.get_custom_type(data)

        if value_custom_type in [StringValueCustomType.data, StringValueCustomType.dict, StringValueCustomType.list]:
            raise ValueError(f"Value {str(data)} of type {type(data)} is not supported in key.")

        if value_custom_type in [
            StringValueCustomType.date, StringValueCustomType.datetime, StringValueCustomType.time
        ]:
            result = data.isoformat()
        elif value_custom_type == StringValueCustomType.enum:
            # get enum short name and cache to type_dict
            short_name = alias_dict[type_] if (type_ := type(data)) in alias_dict else type_.__name__
            type_dict[short_name] = type_

            result = f"{short_name}.{data.name}"
        elif value_custom_type == StringValueCustomType.uuid:
            result = base64.b64encode(data.bytes).decode()
        elif value_custom_type == StringValueCustomType.bytes:
            result = base64.b64encode(data).decode()
        else:
            result = str(data)

        return StringValueParser.add_type_prefix(result, value_custom_type)

    def _deserialize_key_token(self, data: str) -> Any:

        value, value_custom_type = StringValueParser.parse(data)

        if value_custom_type is None:
            return value if value != '' else None

        if value_custom_type == StringValueCustomType.date:
            return dt.date.fromisoformat(value)
        elif value_custom_type == StringValueCustomType.datetime:
            return dt.datetime.fromisoformat(value)
        elif value_custom_type == StringValueCustomType.time:
            return dt.time.fromisoformat(value)
        elif value_custom_type == StringValueCustomType.bool:
            return True if value.lower() == "true" else False
        elif value_custom_type == StringValueCustomType.int:
            return int(value)
        elif value_custom_type == StringValueCustomType.float:
            return float(value)
        elif value_custom_type == StringValueCustomType.enum:
            enum_type, enum_value = value.split(".")
            deserialized_type = type_dict.get(enum_type, None)  # noqa
            if deserialized_type is None:
                raise RuntimeError(
                    f"Enum not found for name or alias '{enum_type}' during key token deserialization. "
                    f"Ensure all serialized enums are included in package import settings."
                )

            # get enum value
            return deserialized_type[enum_value]  # noqa
        elif value_custom_type == StringValueCustomType.uuid:
            return UUID(bytes=base64.b64decode(value.encode()))
        elif value_custom_type == StringValueCustomType.bytes:
            return base64.b64decode(value.encode())
        else:
            return value

    def serialize_key(self, data):
        """Serialize key to string, flattening for composite keys."""

        key_slots = data.get_key_type().__slots__
        result = ";".join(
            self._serialize_key_token(v)  # TODO: Apply rules depending on the specific primitive type
            if (v := getattr(data, k)).__class__.__name__ in primitive_type_names or isinstance(v, Enum)
            else self.serialize_key(v)
            for k in key_slots
        )

        key_short_name = alias_dict[type_] if (type_ := data.get_key_type()) in alias_dict else type_.__name__

        # TODO: consider to have separated cache dict for key types
        type_dict[key_short_name] = type_
        type_token = StringValueParser.add_type_prefix(key_short_name, StringValueCustomType.key)
        return f"{type_token};{result}"

    def substitute_to_slots(self, token_iterator, key_type=None) -> Dict[str, Any]:
        result = {}
        slots_iterator = iter(key_type.__slots__) if key_type else None

        while token := next(token_iterator, None):

            token_value, token_type = StringValueParser.parse(token)

            if token_type == StringValueCustomType.key:

                current_key_type = type_dict.get(token_value, None)  # noqa

                if current_key_type is None:
                    raise RuntimeError(
                        f"Class not found for name or alias '{token_value}' during deserialization. "
                        f"Ensure all serialized classes are included in package import settings."
                    )

                if slots_iterator is None:
                    return self.substitute_to_slots(token_iterator, current_key_type)
                else:
                    slot = next(slots_iterator)
                    result[slot] = self.substitute_to_slots(token_iterator, current_key_type)

            else:
                slot = next(slots_iterator)
                result[slot] = self._deserialize_key_token(token)

        return key_type(**result)


    def deserialize_key(self, data: str) -> KeyProtocol:

        slot_values = self.substitute_to_slots(iter(data.split(";")))

        return slot_values
