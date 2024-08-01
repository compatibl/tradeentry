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
from typing import Any, Type
import datetime as dt

from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.serialization.string_value_parser import StringValueParser, StringValueCustomType
from cl.runtime.storage.data_source_types import TDataset

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
            return ''

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
            result = f"{type(data).__name__}.{data.name}"
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
        else:
            return value

    def serialize_key(self, data):
        """Serialize key to string, flattening for composite keys."""

        key_slots = data.get_key_type().__slots__
        result = ";".join(
            str(v)  # TODO: Apply rules depending on the specific primitive type
            if (v := getattr(data, k)).__class__.__name__ in primitive_type_names or isinstance(v, Enum)
            else self.serialize_key(v)
            for k in key_slots
        )
        return result

    def deserialize_key(self, data: str, key_type: Type) -> KeyProtocol:
        key_slots = key_type.__slots__
        key_tokens = data.split(";")

        # TODO: support nested keys
        if len(key_tokens) > len(key_slots):
            raise ValueError(
                "key tokens len > key slots len. Probably nested keys. Nested keys currently is not supported."
            )

        filled_slots = key_slots[:len(key_tokens)]

        # TODO: deserialize string tokens using specific rules (or annotations?)
        key_fields = {slot: self._deserialize_key_token(token) for slot, token in zip(filled_slots, key_tokens)}
        return key_type(**key_fields)
