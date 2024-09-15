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
from enum import Enum
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Type
from uuid import UUID
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.schema.schema import Schema

# TODO (Roman): remove dependency from dict_serializer
from cl.runtime.serialization.dict_serializer import alias_dict
from cl.runtime.serialization.dict_serializer import get_type_dict
from cl.runtime.serialization.string_value_parser import StringValueCustomType
from cl.runtime.serialization.string_value_parser import StringValueParser

primitive_type_names = ["NoneType", "str", "float", "int", "bool", "date", "time", "datetime", "bytes", "UUID"]
"""Detect primitive type by checking if class name is in this list."""


# TODO: Add checks for custom override of default serializer inside the class
class StringSerializer:
    """Serialize key to string, flattening hierarchical structure."""

    @classmethod
    def _serialize_key_token(cls, data) -> str:
        """Serialize key field to string token."""

        if data is None:
            # TODO (Roman): make different None and empty string
            return ""

        if isinstance(data, str):
            return data

        value_custom_type = StringValueParser.get_custom_type(data)

        if value_custom_type in [StringValueCustomType.data, StringValueCustomType.dict, StringValueCustomType.list]:
            raise ValueError(f"Value {str(data)} of type {type(data)} is not supported in key.")

        if value_custom_type in [
            StringValueCustomType.date,
            StringValueCustomType.datetime,
            StringValueCustomType.time,
        ]:
            result = data.isoformat()
        elif value_custom_type == StringValueCustomType.enum:
            # Get enum short name and cache to type_dict
            short_name = alias_dict[type_] if (type_ := type(data)) in alias_dict else type_.__name__
            type_dict = get_type_dict()
            type_dict[short_name] = type_

            result = f"{short_name}.{data.name}"
        elif value_custom_type == StringValueCustomType.uuid:
            result = str(data)
        elif value_custom_type == StringValueCustomType.bytes:
            result = base64.b64encode(data).decode()
        else:
            result = str(data)

        return StringValueParser.add_type_prefix(result, value_custom_type)

    @classmethod
    def _deserialize_key_token(cls, data: str, custom_type: StringValueCustomType | None) -> Any:
        """Deserialize key string token of custom type."""

        if custom_type is None:
            return data if data != "" else None

        if custom_type == StringValueCustomType.date:
            return dt.date.fromisoformat(data)
        elif custom_type == StringValueCustomType.datetime:
            return dt.datetime.fromisoformat(data)
        elif custom_type == StringValueCustomType.time:
            return dt.time.fromisoformat(data)
        elif custom_type == StringValueCustomType.bool:
            return True if data.lower() == "true" else False
        elif custom_type == StringValueCustomType.int:
            return int(data)
        elif custom_type == StringValueCustomType.float:
            return float(data)
        elif custom_type == StringValueCustomType.enum:
            enum_type, enum_value = data.split(".")
            type_dict = get_type_dict()
            deserialized_type = type_dict.get(enum_type, None)  # noqa
            if deserialized_type is None:
                raise RuntimeError(
                    f"Enum not found for name or alias '{enum_type}' during key token deserialization. "
                    f"Ensure all serialized enums are included in package import settings."
                )

            # get enum value
            return deserialized_type[enum_value]  # noqa
        elif custom_type == StringValueCustomType.uuid:
            return UUID(data)
        elif custom_type == StringValueCustomType.bytes:
            return base64.b64decode(data.encode())
        else:
            return data

    def serialize_key(self, data, add_type_prefix: bool = False):
        """Serialize key to string, flattening for composite keys."""

        key_slots = data.get_key_type().__slots__
        result = ";".join(
            (
                self._serialize_key_token(v)  # TODO: Apply rules depending on the specific primitive type
                if (v := getattr(data, k)).__class__.__name__ in primitive_type_names or isinstance(v, Enum)
                else self.serialize_key(v, add_type_prefix=True)
            )
            for k in key_slots
        )

        if add_type_prefix:
            key_short_name = alias_dict[type_] if (type_ := data.get_key_type()) in alias_dict else type_.__name__

            # TODO (Roman): consider to have separated cache dict for key types
            type_dict = get_type_dict()
            type_dict[key_short_name] = type_
            type_token = StringValueParser.add_type_prefix(key_short_name, StringValueCustomType.key)
            result = f"{type_token};{result}"

        return result

    # TODO (Roman): add errors with description for invalid keys
    def _fill_key_slots(self, tokens_iterator: Iterator[str], type_: Type | None = None) -> Any:
        """
        Sequentially fill slots of key type_ with values from iterator. If type_ is None try to determine type from
        tokens. Values should be in specific format and will be deserialized. Function is recursive for embedded keys.

        Embedded keys are defined by separated tokens in a specific format that contain the type of the embedded key.
        Other tokens contain serialized field values.

        Example:
            KeyType.__slots__ = ("int_field", "str_field", "embedded_key_field", "other_str_field")
            EmbeddedKeyType.__slots__ = ("int_field", "str_field")

            tokens = ("::#key#KeyType", "::#int#1", "str1", "::#key#EmbeddedKeyType", "::#int#2", "str2", "str3")

            Result:
                KeyType(
                    int_field = 1,
                    str_field = "str1",
                    EmbeddedKeyType(
                        int_field = 2,
                        str_field = "str2"
                    ),
                    other_str_field = "str3"
                )
        """

        # contains slot values
        slot_values: Dict[str, Any] = {}

        # init slots iterator if type_ is specified
        slots_iterator = iter(type_.__slots__) if type_ else None

        # reserve first slot from slots iterator
        slot = next(slots_iterator) if slots_iterator else None

        # iterate over tokens using tokens iterator
        while token := next(tokens_iterator, None):
            # parse token to value and custom type
            token, token_type = StringValueParser.parse(token)

            # if token is key get type and fill embedded key slots recursively using the same iterator instance
            if token_type == StringValueCustomType.key:
                # TODO (Roman): verify proper way to get type in serialization.
                current_type = Schema.get_type_by_short_name(token)

                if current_type is None:
                    raise RuntimeError(
                        f"Class not found for name or alias '{token}' during key deserialization. "
                        f"Ensure all serialized classes are included in package import settings."
                    )

                key = self._fill_key_slots(tokens_iterator, current_type)

                # slots_iterator - None, means the root key object, so return it, otherwise assign the associated slot
                if slots_iterator is None:
                    return key
                else:
                    slot_values[slot] = key
            else:
                # deserialize token and assign the associated slot
                slot_values[slot] = self._deserialize_key_token(token, token_type)

            # reserve next slot for next token
            slot = next(slots_iterator, None)

            # if the slots are over - break.
            if slot is None:
                break

        # construct final key object
        return type_(**slot_values)

    def deserialize_key(self, data: str, type_: Type | None = None) -> KeyProtocol:
        """Deserialize key object from string representation."""

        return self._fill_key_slots(iter(data.split(";")), type_)
