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
from cl.runtime import ClassInfo
from cl.runtime.records.dataclasses_extensions import field, missing
from cl.runtime.schema.field_kind import FieldKind
from dataclasses import dataclass
from enum import Enum
from typing import Literal
from typing import Type
from typing_extensions import Self
from uuid import UUID

primitive_types = [str, float, bool, int, dt.date, dt.time, dt.datetime, UUID, bytes]
"""List of primitive types."""

primitive_modules = ["builtins", "datetime", "uuid"]
"""List of modules for primitive types."""


@dataclass(slots=True, kw_only=True)
class FieldDecl:
    """Field declaration."""

    name: str = missing()
    """Field name."""

    label: str | None = missing()
    """Field label (if not specified, titleized name is used instead)."""

    comment: str | None = missing()
    """Field comment."""

    field_kind: FieldKind = missing()
    """Kind of the element within the container if the field is a container, otherwise kind of the field itself."""

    field_type: str = missing()
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
    def create(
        cls,
        record_type: Type,
        field_name: str,
        field_type: Type,
        field_comment: str,
        *,
        dependencies: typing.Set[Type] | None = None,
    ) -> Self:
        """
        Create from field name and type.

        Args:
            record_type: Type of the record for which the field is defined
            field_name: Name of the field
            field_type: Type of the field obtained from get_type_hints where ForwardRefs are resolved
            field_comment: Field comment (docstring), currently requires source parsing due Python limitations
            dependencies: Set of types used in field or methods of the specified type, populated only if not None
        """

        from cl.runtime.schema.schema import Schema  # TODO: Avoid circlular dependency

        result = cls()
        result.name = field_name.removesuffix("_")
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
        if field_origin is Literal:
            # List of literal strings
            result.field_kind = "primitive"
            result.field_type = str.__name__

        elif field_origin is tuple:
            # Generic key
            result.field_kind = "primitive"
            result.field_type = "key"

        elif field_origin is None:
            # Assign element kind
            if field_type in primitive_types:
                # Indicate that field is one of the supported primitive types
                result.field_kind = "primitive"
            elif issubclass(field_type, Enum):
                # Indicate that field is an enum
                result.field_kind = "enum"
            elif field_type.__name__.endswith("Key"):
                # Indicate that field is a key
                result.field_kind = "key"
            else:
                # Indicate that field is a user-defined data or record
                result.field_kind = "data"

            if field_type.__module__ in primitive_modules:
                # Primitive type, specify type name
                result.field_type = field_type.__name__
            else:
                # Complex type, specify full class path
                field_class_path = f"{field_type.__module__}.{field_type.__name__}"

                # For keys, remove suffix
                if result.field_kind == "key":
                    if field_class_path.endswith("Key"):
                        field_class_module = field_type.__module__.removesuffix("_key")
                        field_class_name = field_type.__name__.removesuffix("Key")
                        field_class_path = f"{field_class_module}.{field_class_name}"
                    else:
                        raise RuntimeError("Field has TypeKind=key but class name does not end in 'Key'.")

                result.field_type = field_class_path
                field_type_obj = ClassInfo.get_class_type(field_class_path)

                if (
                    dependencies is not None
                    and field_type_obj is not record_type
                    and field_type_obj not in dependencies
                ):
                    # TODO: Do we need this if we are processing dependencies?
                    # TODO: Should a list of dependencies be added to TypeDecl object directly
                    if issubclass(field_type_obj, Enum):
                        from cl.runtime.schema.enum_decl import EnumDecl

                        # TODO: Restore call when implemented EnumDecl.for_type(field_type_obj, dependencies=dependencies)
                    else:
                        from cl.runtime.schema.type_decl import TypeDecl

                        TypeDecl.for_type(field_type_obj, dependencies=dependencies)

                # Add to dependencies
                if dependencies is not None:
                    dependencies.add(field_type_obj)

                # Add to Schema

        else:
            raise RuntimeError(f"Complex type {field_type} is not recognized when building data source schema.")

        return result
