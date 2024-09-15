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
import types
from dataclasses import dataclass
from typing import Type
from typing import Union
from typing import get_args
from typing import get_origin
from memoization import cached
from typing_extensions import Self
from cl.runtime.primitive.primitive_util import PrimitiveUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.schema.member_decl import MemberDecl
from cl.runtime.schema.value_decl import ValueDecl


@dataclass(slots=True, kw_only=True)
class HandlerVariableDecl(MemberDecl):
    """Handler parameter or return variable declaration."""

    vector: bool | None = missing()  # TODO: Similar change to vector in element decl
    """Flag indicating variable size array (vector) container."""

    optional: bool | None = missing()
    """Flag indicating optional element."""

    label: str | None = missing()
    """Parameter label."""

    comment: str | None = missing()
    """Parameter comment. Contains addition information about handler parameter."""

    @classmethod
    @cached
    def create(cls, value_type: Type, record_type: Type) -> Self:
        """
        Create from field name and type.

        Args:
            value_type: Type of the value
        """
        from cl.runtime.schema.type_decl import TypeDecl

        result = cls()

        # Get origin and args of the field type
        value_type_ = value_type
        type_origin = get_origin(value_type_)
        type_args = get_args(value_type_)

        # Note two possible forms of origin for optional, typing.Union and types.UnionType
        is_union = type_origin is Union or type_origin is types.UnionType
        is_optional = is_union and type(None) in type_args

        # Strip optional from field_type
        if is_optional:
            # Indicate that field can be None
            result.optional = True

            # Get type information without None
            value_type_ = type_args[0]
            type_origin = get_origin(value_type_)
            type_args = get_args(value_type_)
        else:
            # Indicate that field cannot be None
            result.optional = False

        # Check for one of the supported container types
        if type_origin is list:
            # Get the type of value inside the container
            value_type_ = type_args[0]
        else:
            # No container
            result.vector = False

        # Check if value_type is Self
        if value_type_ == Self:
            value_type_ = record_type

        # Handle primitive types
        # TODO (Ina): Add Enum and Dict supporting, handle unexpected types
        if PrimitiveUtil.is_primitive(value_type_):
            result.value = ValueDecl.create(value_type_)
        elif value_type_.__name__.endswith("Key"):
            result.key_ = TypeDecl.for_type(value_type_, skip_handlers=True)
        elif inspect.isclass(value_type_):
            result.data = TypeDecl.for_type(value_type_, skip_handlers=True)
        else:
            raise Exception(f"Unexpected handler type {value_type_.__name__}.")

        return result
