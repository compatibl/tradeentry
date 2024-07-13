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
from typing import Tuple

primitive_type_names = ["NoneType", "str", "float", "int", "bool", "date", "time", "datetime", "bytes", "UUID"]
"""Detect primitive type by checking if class name is in this list."""


# TODO: Add checks for to_node, from_node implementation for custom override of default serializer
class StringSerializer:
    """Serialize key."""

    def serialize_key(self, data):
        """Serialize key to string, flattening for composite keys."""

        key_slots = data.get_key_type().__slots__
        result = ";".join(
            str(v)  # TODO: Apply rules depending on the specific primitive type
            if (v := getattr(data, k)).__class__.__name__ in primitive_type_names
            else v.name
            if isinstance(v, Enum)
            else self.serialize_key(v)
            for k in key_slots
        )
        return result
