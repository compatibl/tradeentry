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

from enum import IntEnum
from typing import TYPE_CHECKING, Any, Type

from cl.runtime.primitive.string_util import to_pascal_case, to_snake_case
from cl.runtime.schema.docstring_parser import parse_method_docstring

if TYPE_CHECKING:
    from cl.runtime.serialization.method_info import MethodInfo


def element_name_to_schema(field_: Any) -> str:
    """Process attribute field name to correct schema name."""
    metadata_name: str = field_.metadata.get('name', None)
    if metadata_name:
        return metadata_name
    return to_pascal_case(field_.name)


def enum_name_to_schema(enum_: IntEnum) -> str:
    """Process enum item name to correct schema name."""
    enum_value = enum_.name
    if enum_value.endswith('_'):
        return enum_value[:-1]
    return enum_value


def enum_name_from_schema(cls: Type[IntEnum], value: str) -> IntEnum:
    """Process enum item name to correct schema name."""
    if value in ('False', 'None', 'True'):
        return cls[value + '_']
    else:
        return cls[value]


def param_name_from_schema(schema_param_name: str, method_info: 'MethodInfo'):
    """
    Map a schema parameter name to the corresponding method parameter name based on the method's docstring.

    Parameters:
        schema_param_name (str): The schema parameter name.
        method_info (MethodInfo): Information about the method, including its docstring.

    Returns:
        str: The corresponding method parameter name, or a snake_case version of the schema_param_name if not found.
    """
    parsed_doc = parse_method_docstring(method_info.docstring)
    for param_name, param_doc in parsed_doc.parameters.items():
        if param_doc.meta.get('name', '') == schema_param_name:
            return param_name
    return to_snake_case(schema_param_name)
