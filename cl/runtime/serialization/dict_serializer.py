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
from cl.runtime.storage.data_source_types import TDataDict
from dataclasses import dataclass
from enum import Enum
from inflection import camelize
from typing import Dict
from typing import Type


class MissingType:
    """Type representing a missing value."""


missing = MissingType()
"""Represents missing value distinct from None."""

primitive_type_names = ["NoneType", "str", "float", "int", "bool", "date", "time", "datetime", "bytes", "UUID"]
"""Detect primitive type by checking if class name is in this list."""

# TODO: Initialize from settings
alias_dict: Dict[Type, str] = dict()
"""Dictionary of class name aliases using type as key (includes classes and enums with aliases only)."""

# TODO: Initialize from settings
type_dict: Dict[str, Type] = dict()
"""Dictionary of types using class name or alias as key (includes all classes and enums)."""

def get_all_slots(cls):
    # Initialize an empty set to collect slot names
    slots = set()

    # Traverse the class hierarchy
    for base in cls.__mro__:
        if hasattr(base, '__slots__'):
            # Add slots from the current class
            if isinstance(base.__slots__, str):
                slots.add(base.__slots__)
            else:
                slots.update(base.__slots__)

    return list(slots)


# TODO: Add checks for to_node, from_node implementation for custom override of default serializer
@dataclass(slots=True, kw_only=True)
class DictSerializer:
    """Serialization for slots-based classes (including dataclasses with slots=True)."""

    pascalize_keys: bool = False
    """If true, pascalize keys during serialization."""

    def serialize_data(self, data):  # TODO: Check if None should be supported
        """Serialize to dictionary containing primitive types, dictionaries, or iterables."""

        if (slots := getattr(data, "__slots__", None)) is not None:
            # Slots class, serialize as dictionary
            # Get slots from this class and its bases in the order of declaration from base to derived
            all_slots = get_all_slots(data.__class__)
            # Serialize slot values in the order of declaration except those that are None
            result = {
                k
                if not self.pascalize_keys
                else camelize(k, uppercase_first_letter=True): v
                if v.__class__.__name__ in primitive_type_names
                else self.serialize_data(v)
                for k in all_slots
                if (v := getattr(data, k)) is not None
            }
            # To find short name, use 'in' which is faster than 'get' when most types do not have aliases
            short_name = alias_dict[type_] if (type_ := data.__class__) in alias_dict else type_.__name__
            # Cache type for subsequent reverse lookup
            type_dict[short_name] = type_
            # Add to result
            result["_type"] = short_name
            return result
        elif isinstance(data, dict):
            # Dictionary, return with serialized values
            result = {
                k: v if v.__class__.__name__ in primitive_type_names else self.serialize_data(v)
                for k, v in data.items()
            }
            return result
        elif hasattr(data, "__iter__"):
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
                return [v if v.__class__.__name__ in primitive_type_names else self.serialize_data(v) for v in data]
        elif isinstance(data, Enum):
            # Serialize enum as a dict using enum class short name and item name (rather than item value)
            # To find short name, use 'in' which is faster than 'get' when most types do not have aliases
            short_name = alias_dict[type_] if (type_ := type(data)) in alias_dict else type_.__name__
            # Cache type for subsequent reverse lookup
            type_dict[short_name] = type_
            return {"_enum": short_name, "_name": data.name}
        else:
            raise RuntimeError(f"Cannot deserialize data of type '{type(data)}'.")

    def deserialize_data(self, data: TDataDict):  # TODO: Check if None should be supported
        """Deserialize from dictionary containing primitive types, dictionaries, or iterables."""

        if self.pascalize_keys:
            raise RuntimeError("Cannot deserialize if pascalize_keys=True.")

        if isinstance(data, dict):
            # Determine if the dictionary is a serialized dataclass or a dictionary
            if (short_name := data.get("_type", None)) is not None:
                # If _type is specified, create an instance of _type after deserializing fields recursively
                deserialized_type = type_dict.get(short_name, None)  # noqa
                if deserialized_type is None:
                    raise RuntimeError(
                        f"Class not found for name or alias '{short_name}' during deserialization. "
                        f"Ensure all serialized classes are included in package import settings."
                    )
                deserialized_fields = {
                    k: v if v.__class__.__name__ in primitive_type_names else self.deserialize_data(v)
                    for k, v in data.items()
                    if k != "_type"
                }
                result = deserialized_type(**deserialized_fields)  # noqa
                return result
            elif (short_name := data.get("_enum", None)) is not None:
                # If _enum is specified, create an instance of _enum using _name
                deserialized_type = type_dict.get(short_name, None)  # noqa
                if deserialized_type is None:
                    raise RuntimeError(
                        f"Enum not found for name or alias '{short_name}' during deserialization. "
                        f"Ensure all serialized enums are included in package import settings."
                    )
                result = deserialized_type[data["_name"]]  # noqa
                return result
            else:
                # Otherwise return a dictionary with recursively deserialized values
                result = {
                    k: v if v.__class__.__name__ in primitive_type_names else self.deserialize_data(v)
                    for k, v in data.items()
                }
                return result
        elif hasattr(data, "__iter__"):
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
                return [v if v.__class__.__name__ in primitive_type_names else self.deserialize_data(v) for v in data]
        else:
            raise RuntimeError(f"Cannot deserialize data of type '{type(data)}'.")
