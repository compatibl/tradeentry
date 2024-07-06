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


class MissingType:
    """Type representing a missing value."""


missing = MissingType()
"""Represents missing value distinct from None."""

primitive_type_names = ["NoneType", "str", "float", "int", "bool", "date", "time", "datetime", "bytes", "UUID"]
"""Detect primitive type by checking if class name is in this list."""


# TODO: Add checks for to_node, from_node implementation for custom override of default serializer
class SlotsSerializer:
    """Serialization for slots-based classes (including dataclasses with slots=True)."""

    def serialize(self, data):
        """Serialize to dictionary containing primitive types, dictionaries, or iterables."""

        if data.__class__.__name__ in primitive_type_names:
            # Do nothing for None or primitive types
            return data
        elif hasattr(data, "__slots__"):
            # Slots class, return a dictionary of serialized values
            result = {k: self.serialize(getattr(data, k)) for k in data.__slots__}
            # Add type to the result
            result["_type"] = data.__class__
            return result
        elif isinstance(data, dict):
            # Dictionary, return with serialized values
            result = {k: self.serialize(v) for k, v in data.items()}
            return result
        elif hasattr(data, '__iter__'):
            # Get the first item without iterating over the entire sequence
            first_item = next(iter(data), missing)
            if first_item == missing:
                # Empty iterable, return None
                return None
            elif first_item is not None and first_item.__class__.__name__ in primitive_type_names:
                # Performance optimization to skip deserialization for arrays of primitive types
                # based on the type of first item (assumes that all remaining items are also primitive)
                return data
            else:
                # Serialize each element of the iterable
                return [self.serialize(item) for item in data]
        elif isinstance(data, Enum):
            # Enum, serialize as name
            return {"_enum": type(data), "_name": data.name}
        else:
            raise RuntimeError(f"Cannot deserialize data of type '{type(data)}'.")

    def deserialize(self, data):
        """Deserialize from dictionary containing primitive types, dictionaries, or iterables."""

        if data.__class__.__name__ in primitive_type_names:
            # Do nothing for None or primitive types
            return data
        elif isinstance(data, dict):
            # Determine if the dictionary is a serialized dataclass or a dictionary
            if (deserialized_type := data.get("_type", None)) is not None:
                # If _type is specified, create an instance of _type after deserializing fields recursively
                deserialized_fields = {k: self.deserialize(v) for k, v in data.items() if k != "_type"}
                result = deserialized_type(**deserialized_fields)  # noqa
                return result
            elif (deserialized_enum := data.get("_enum", None)) is not None:
                # If _enum is specified, create an instance of _enum using _name
                result = deserialized_enum[data["_name"]] # noqa
                return result
            else:
                # Otherwise return a dictionary with recursively deserialized values
                result = {k: self.deserialize(v) for k, v in data.items()}
                return result
        elif hasattr(data, '__iter__'):
            # Get the first item without iterating over the entire sequence
            first_item = next(iter(data), missing)
            if first_item == missing:
                # Empty iterable, return None
                return None
            elif first_item is not None and first_item.__class__.__name__ in primitive_type_names:
                # Performance optimization to skip deserialization for arrays of primitive types
                # based on the type of first item (assumes that all remaining items are also primitive)
                return data
            else:
                # Deserialize each element of the iterable
                return [self.deserialize(item) for item in data]
        else:
            raise RuntimeError(f"Cannot deserialize data of type '{type(data)}'.")
