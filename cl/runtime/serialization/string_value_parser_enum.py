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

import re
from enum import Enum
from enum import IntEnum
from types import DynamicClassAttribute
from typing import Any
from typing import Dict
from typing import Final
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.records.protocols import is_key
from cl.runtime.serialization.dict_serializer import DictSerializer


class StringValueCustomTypeEnum(IntEnum):
    """Custom types supported for string representation."""

    DATA = 0
    """Data type."""

    DICT = 1
    """Dict type."""

    LIST = 2
    """Vector type."""

    DATE = 3
    """Date type."""

    DATETIME = 4
    """Datetime type."""

    TIME = 5
    """Time type."""

    BOOL = 6
    """Bool type."""

    UUID = 7
    """UUID type."""

    ENUM = 8
    """Enum type."""

    BYTES = 9
    """Binary type."""

    INT = 10
    """Integer type."""

    FLOAT = 11
    """Float type."""

    KEY = 12
    """Key type."""


CUSTOM_TYPE_NAME_TO_VALUE: Final[Dict[str, StringValueCustomTypeEnum]] = {
    # CaseUtil.upper_to_snake_case(member.name): member for member in StringValueCustomTypeEnum
    "bool": StringValueCustomTypeEnum.BOOL,
    "json": StringValueCustomTypeEnum.DICT,
}
"""Name to enum value mapping."""

CUSTOM_TYPE_VALUE_TO_NAME: Final[Dict[StringValueCustomTypeEnum, str]] = {
    v: k for k, v in CUSTOM_TYPE_NAME_TO_VALUE.items()
}
"""Enum value to name mapping."""


class StringValueParser:
    """Parser for string value representations of custom types."""

    @classmethod
    def add_type_prefix(cls, value: str, type_: StringValueCustomTypeEnum | None) -> str:
        """Add type prefix to value that is a string representation of object of type type_."""

        if type_ is None:
            return value

        # Check type name in alias mapping
        type_name = (
            type_name_alias if ((type_name_alias := CUSTOM_TYPE_VALUE_TO_NAME.get(type_)) is not None) else type_.name
        )

        type_prefix = f"```{type_name} "
        return type_prefix + DictSerializer._serialize_primitive(value, type_name)

    @classmethod
    def parse(cls, value: str) -> (str, StringValueCustomTypeEnum | None):
        """
        Check if value is a string representation of some custom type and parse it to separated objects:
            value without type and value type.

        Examples:
            "```bool True" -> "True", bool
            "True" -> "True", None
            "any_string_without_prefix" -> "any_string_without_prefix", None
        """

        # Check if value starts with type info prefix using regex
        typed_value_pattern = re.compile("```(?P<type>.*?) .*")
        typed_value_match = typed_value_pattern.match(value)

        if typed_value_match:
            # get custom type name according to pattern
            value_custom_type = typed_value_match.group("type")

            # remove type prefix from value
            value_without_prefix = value.removeprefix(f"```{value_custom_type} ")

            # Check custom type in alias mapping
            value_custom_type = (
                custom_type
                if ((custom_type := CUSTOM_TYPE_NAME_TO_VALUE.get(value_custom_type)) is not None)
                # TODO: Use CaseUtil.snake_to_upper_case when case is standardized
                else StringValueCustomTypeEnum[value_custom_type.upper()]
            )

            return value_without_prefix, value_custom_type
        else:
            # return unmodified value and custom type None
            return value, None

    @classmethod
    def get_custom_type(cls, value: Any) -> StringValueCustomTypeEnum | None:
        """Determine custom_type of value."""
        if value.__class__.__name__ == "date":
            return StringValueCustomTypeEnum.DATE
        elif value.__class__.__name__ == "datetime":
            return StringValueCustomTypeEnum.DATETIME
        elif value.__class__.__name__ == "time":
            return StringValueCustomTypeEnum.TIME
        elif value.__class__.__name__ == "bool":
            return StringValueCustomTypeEnum.BOOL
        elif value.__class__.__name__ == "int":
            return StringValueCustomTypeEnum.INT
        elif value.__class__.__name__ == "float":
            return StringValueCustomTypeEnum.FLOAT
        elif value.__class__.__name__ == "UUID":
            return StringValueCustomTypeEnum.UUID
        elif value.__class__.__name__ == "bytes":
            return StringValueCustomTypeEnum.BYTES
        elif is_key(value):
            return StringValueCustomTypeEnum.KEY
        elif hasattr(value, "__slots__"):
            return StringValueCustomTypeEnum.DATA
        elif isinstance(value, dict):
            return StringValueCustomTypeEnum.DICT
        elif isinstance(value, Enum):
            return StringValueCustomTypeEnum.ENUM
        elif hasattr(value, "__iter__"):
            return StringValueCustomTypeEnum.LIST
