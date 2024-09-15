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

import inspect
from typing import Dict
from typing import Type
from memoization import cached


class PrimitiveUtil:
    """
    This class provides all primitive type names and provide methods for type checking.
    """

    primitive_type_map: Dict[str, str] = {
        "str": "String",
        "float": "Double",
        "bool": "Bool",
        "int": "Int",
        "long": "Long",
        "date": "Date",
        "time": "Time",
        "datetime": "DateTime",
        "UUID": "UUID",  # TODO: Check for support in ElementDecl
        "bytes": "Binary",
    }
    """
    Constant representing all primitive type names as they are named in Python with their Runtime names.
    """

    @classmethod
    @cached
    def is_primitive(cls, type_: Type | str) -> bool:
        """Check if the provided type is primitive."""

        type_name = type_.__name__ if inspect._is_type(type_) else type_  # noqa
        return type_name in cls.primitive_type_map

    @classmethod
    @cached
    def get_runtime_name(cls, type_: Type | str) -> str:
        """Return type's Runtime name."""

        type_name = type_.__name__ if inspect._is_type(type_) else type_  # noqa
        if not cls.is_primitive(type_name):
            raise RuntimeError(f"Primitive type {type_name} is not supported.")
        return cls.primitive_type_map.get(type_name)
