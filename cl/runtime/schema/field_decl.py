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

import datetime as dt
import types
import typing
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from dataclasses import dataclass
from enum import Enum
from typing import Literal
from typing import Type
from typing_extensions import Self
from uuid import UUID

from cl.runtime.schema.field_kind import FieldKind

primitive_types = [str, float, bool, int, dt.date, dt.time, dt.datetime, UUID, bytes]
"""List of primitive types."""

primitive_modules = ["builtins", "uuid"]
"""List of modules for primitive types."""


@dataclass(slots=True, kw_only=True)
class FieldDecl:
    """Field declaration."""

    name: str = datafield()
    """Field name."""

    label: str | None = datafield()
    """Field label (if not specified, titleized name is used instead)."""

    comment: str | None = datafield()
    """Field comment."""

    field_kind: FieldKind = datafield()
    """Kind of the element within the container if the field is a container, otherwise kind of the field itself."""

    field_type: str = datafield()
    """Field type name for builtins and uuid modules and module.ClassName for all other types."""

    container_type: str | None = None
    """Container type name for builtins module and module.ClassName for other types."""

    optional_field: bool = False
    """Indicates if the entire field can be None."""

    optional_values: bool = False
    """Indicates if values within the container can be None if the field is a container, otherwise None."""

    additive: bool = False
    """Optional flag indicating if the element is additive (i.e., its sum across records has meaning)."""

    formatter: str | None = None
    """Format string used to display the element using Python conventions ."""

    alternate_of: str | None = None
    """This field is an alternate of the specified field, of which only one can be specified."""

    @classmethod
    def create(cls, record_type: Type, field_name: str, field_type: Type, field_comment: str) -> Self:
        """
        Create from field name and type.

        Args:
            record_type: Type of the record for which the field is defined
            field_name: Name of the field
            field_type: Type of the field obtained from get_type_hints where ForwardRefs are resolved
            field_comment: Field comment (docstring), currently requires source parsing due Python limitations
        """

        result = cls()
        result.name = field_name
        result.comment = field_comment

        # Get origin and args of the field type
        field_origin = typing.get_origin(field_type)
        field_args = typing.get_args(field_type)

        # Note two possible forms of origin for optional, typing.Union and types.UnionType
        is_union = field_origin is typing.Union or field_origin is types.UnionType
        is_optional = is_union and type(None) in field_args

        # Strip optional from field_type
        if is_optional:
            # Indicate that field can be None
            result.optional_field = True

            # Get type information without None
            field_type = field_args[0]
            field_origin = typing.get_origin(field_type)
            field_args = typing.get_args(field_type)
        else:
            # Indicate that field cannot be None
            result.optional_field = False

        # Check for one of the supported container types
        if field_origin in [list, dict]:
            if field_origin.__module__ == "builtins":
                result.container_type = field_origin.__name__
            else:
                result.container_type = f"{field_origin.__module__}.{field_origin.__name__}"

            # Strip container information from field_type to get the type of value inside the container
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
            # Indicate that values can be None
            result.optional_values = True

            # Get type information without None
            field_type = field_args[0]
            field_origin = typing.get_origin(field_type)
            field_args = typing.get_args(field_type)
        else:
            # Indicate that values cannot be None
            result.optional_values = False

        # Parse the value itself
        if field_origin is tuple:
            # Indicate that field is a key
            result.field_kind = "key"

            # Get the first argument of Tuple
            if len(field_args) == 0:
                raise RuntimeError(f"Empty tuple is provided as value for field {field_name}")
            field_arg = field_args[0]

            # One level deeper
            field_origin = typing.get_origin(field_arg)
            if isinstance(field_origin, type):
                # Extract SampleType from Type[SampleType] or Type['SampleType']
                field_args = typing.get_args(field_arg)
                if len(field_args) == 0:
                    raise RuntimeError(
                        f"Type without arguments is provided as value for key field {field_name}, "
                        f"use Type[SampleType] or Type['SampleType'] instead."
                    )

                # Get the argument of Type
                field_arg = field_args[0]
                if isinstance(field_arg, typing.ForwardRef):
                    # For ForwardRef, extract the argument
                    field_arg = field_arg.__forward_arg__
            else:
                raise RuntimeError(f"First element of key tuple for field {field_name} is not a type.")

            if field_arg.__module__.endswith("_key"):
                module_name = field_arg.__module__.removesuffix("_key")
            else:
                raise RuntimeError(f"The module of table class {field_arg.__module__} does not have the suffix _key.")

            if field_arg.__name__.endswith("Table"):
                type_name = field_arg.__name__.removesuffix("Table")
            else:
                raise RuntimeError(f"The name of table class {field_arg.__name__} does not have the suffix Table.")

            result.field_type = f"{module_name}.{type_name}"

        elif field_origin is None:
            # Assign element kind
            if field_type in primitive_types:
                # Indicate that field is one of the supported primitive types
                result.field_kind = "primitive"
            elif issubclass(field_type, Enum):
                # Indicate that field is an enum
                result.field_kind = "enum"
            else:
                # Indicate that field is a user-defined data or record
                result.field_kind = "data"

            if field_type.__module__ in primitive_modules:
                result.field_type = field_type.__name__
            else:
                result.field_type = f"{field_type.__module__}.{field_type.__name__}"

        else:
            raise RuntimeError(f"Complex type {field_type} is not recognized when building data source schema.")

        return result
