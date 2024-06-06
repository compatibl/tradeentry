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

import types
import typing
import datetime as dt
from dataclasses import dataclass
from enum import Enum
from typing import Literal, Type
from typing_extensions import Self
from cl.runtime.records.dataclasses.dataclass_mixin import datafield


@dataclass(slots=True, kw_only=True)
class FieldDecl:
    """Field declaration."""

    name: str = datafield()
    """Field name."""

    label: str | None = datafield()
    """Field label (if not specified, titleized name is used instead)."""

    comment: str | None = datafield()
    """Field comment."""

    field_kind: Literal["primitive", "key", "data", "enum"] = datafield()
    """Kind of the element within the container if the field is a container, otherwise kind of the field itself."""

    field_type: Type = datafield()
    """Type of the element within the container if the field is a container, otherwise type of the field itself."""

    container_type: Type | None = None
    """Type of the container (list, dict, etc.) if the field is a container, otherwise None."""

    optional_field: bool = False
    """Indicates if the entire field can be None."""

    optional_values: bool = False
    """Indicates if values within the container can be None if the field is a container, otherwise None."""

    additive: bool = False
    """Optional flag indicating if the element is additive (i.e., its sum across records has meaning)."""

    format_: str | None = None
    """Format string used to display the element using Python conventions ."""

    alternate_of: str | None = None
    """This field is an alternate of the specified field, of which only one can be specified."""
    
    @classmethod
    def create(cls, field_name: str, field_type: Type) -> Self:
        """
        Create from field name and type.

        Notes:
            The Field object also contains the type but if it is a ForwardRef, it will not be resolved.

        Args:
            field_name: Name of the field
            field_type: Type of the field obtained from get_type_hints where ForwardRefs are resolved
        """
        
        result = cls()
        result.name = field_name

        field_origin = typing.get_origin(field_type)
        field_args = typing.get_args(field_type)

        # Note two possible forms of origin for optional, typing.Union and types.UnionType
        is_union = field_origin is typing.Union or field_origin is types.UnionType
        is_optional = is_union and type(None) in field_args

        # Strip optional from field_type
        if is_optional:
            # Field can be None
            result.optional_field = True
            # Get type information without None
            field_type = field_args[0]
            field_origin = typing.get_origin(field_type)
            field_args = typing.get_args(field_type)
        else:
            # Field cannot be None
            result.optional_field = False

        # Strip container information from field_type to get the type of value inside the container
        if field_origin in [list, dict]:
            # One of the supported container types
            result.container_type = field_origin
            field_type = field_args[0]
            field_origin = typing.get_origin(field_type)
            field_args = typing.get_args(field_type)
        else:
            # No container
            result.container_type = None

        # Strip optional again from the inner type
        is_union = field_origin is typing.Union or field_origin is types.UnionType
        is_optional = is_union and type(None) in field_args
        if is_optional:
            # Values can be None
            result.optional_values = True
            # Get type information without None
            field_type = field_args[0]
            field_origin = typing.get_origin(field_type)
            field_args = typing.get_args(field_type)
        else:
            # Values cannot be None
            result.optional_values = False

        # Parse the value itself
        if field_origin is tuple:
            # Key is represented as a tuple
            result.field_kind = "key"

            # Get the first argument of Tuple
            tuple_args = typing.get_args(field_type)
            if len(tuple_args) == 0:
                raise RuntimeError(f"Empty tuple is provided as value for field {field_name}")
            tuple_arg = tuple_args[0]

            type_origin = typing.get_origin(tuple_arg)
            if isinstance(type_origin, type):
                # Extract SampleType from Type[SampleType] or Type['SampleType']
                type_args = typing.get_args(tuple_arg)
                if len(type_args) == 0:
                    raise RuntimeError(
                        f"Type without arguments is provided as value for key field {field_name}, "
                        f"use Type[SampleType] or Type['SampleType'] instead."
                    )

                # Get the argument of Type
                type_arg = type_args[0]
                if isinstance(type_arg, typing.ForwardRef):
                    # For ForwardRef, extract the argument
                    type_arg = type_arg.__forward_arg__

            else:
                raise RuntimeError(f"First element of key tuple for field {field_name} is not a type.")

            # Assign key type
            result.field_type = type_arg

        elif field_origin is None:
            # Assign element kind
            if field_type in [str, float, bool, int, dt.date, dt.time, dt.datetime]:
                # One of the supported primitive types
                result.field_kind = "primitive"
            elif issubclass(field_type, Enum):
                # Enum
                result.field_kind = "enum"
            else:
                # User-defined data or record
                result.field_kind = "data"

            # Assign element type
            result.field_type = field_type

        else:
            raise RuntimeError(f"Complex type {field_type} is not recognized when building data source schema.")

        return result
