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

from __future__ import annotations

import ast
import inspect
import textwrap

from cl.runtime import KeyUtil
from cl.runtime.records.dataclasses.dataclass_mixin import DataclassMixin
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.schema.display_kind import DisplayKind
from cl.runtime.schema.element_decl import ElementDecl
from cl.runtime.schema.field_decl import FieldDecl
from cl.runtime.schema.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.schema.module_decl import ModuleDecl
from cl.runtime.schema.module_decl_key import ModuleDeclKey
from cl.runtime.schema.type_decl_key import TypeDeclKey, TypeDeclTable
from cl.runtime.schema.type_index_decl import TypeIndexDecl
from cl.runtime.schema.type_kind import TypeKind
from dataclasses import dataclass
from enum import Enum
from inflection import titleize
from memoization import cached
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Type
from typing import get_type_hints
from typing_extensions import Self


def for_type_key_maker(cls, record_type: Type, *, skip_fields: bool = False) -> str:
    """Custom key marker for 'for_type' class method."""
    return f"{record_type.__module__}.{record_type.__name__}.{skip_fields}"


@dataclass(slots=True, kw_only=True)
class TypeDecl(DataclassMixin):
    """
    Defines type declaration. A tag of entity type XML representation corresponds to each element of the type. The
    names of type elements and corresponding tags coincide.
    """

    module: ModuleDeclKey = datafield()  # TODO: Merge with name to always use full name
    """Module reference."""

    name: str = datafield()
    """Type name is unique when combined with module."""

    label: str | None = datafield()
    """Type label."""

    comment: str | None = datafield()
    """Type comment. Contains additional information."""

    kind: TypeKind | None = datafield()
    """Type kind."""

    display_kind: DisplayKind = datafield()  # TODO: Make optional, treat None as Basic
    """Display kind."""

    inherit: TypeDeclKey | None = datafield()
    """Parent type reference."""

    declare: HandlerDeclareBlockDecl | None = datafield()  # TODO: Flatten or use block for abstract flag
    """Handler declaration block."""

    elements: List[ElementDecl] | None = datafield()  # TODO: Consider renaming to fields
    """Element declaration block."""

    keys: List[str] | None = datafield()
    """Array of key element names (specify in base class only)."""

    indexes: List[TypeIndexDecl] | None = datafield()
    """Defines indexes for the type."""

    immutable: bool | None = datafield()
    """Immutable flag."""

    permanent: bool | None = datafield()
    """When the record is saved, also save it permanently."""

    def get_key(self) -> TypeDeclKey:
        return TypeDeclTable, self.module, self.name

    @classmethod
    def for_key(cls, key: TypeDeclKey) -> Self:
        """Create or return cached object for the specified type declaration key."""
        class_path = f"{key[1][1]}.{key[2]}"  # TODO: Use parse_key method
        return cls.for_class_path(class_path)

    @classmethod
    def for_class_path(cls, class_path: str) -> Self:
        """Create or return cached object for the specified class path in module.ClassName format."""
        raise NotImplementedError()

    @classmethod
    @cached(custom_key_maker=for_type_key_maker)
    def for_type(cls, record_type: Type, *, skip_fields: bool = False) -> Self:
        """
        Create or return cached object for the specified record type.

        Args:
            record_type: Type of the record for which the declaration is created
            skip_fields: Use this flag to skip fields generation when the method is invoked from a derived class
        """

        if issubclass(record_type, Enum):
            raise RuntimeError(f"Cannot create TypeDecl for class {record_type.__name__} because it is an enum.")
        if issubclass(record_type, tuple):
            raise RuntimeError(f"Cannot create TypeDecl for class {record_type.__name__} because it is a tuple.")

        # Create instance of the final type
        result = cls()

        result.module = ModuleDecl, record_type.__module__
        result.name = record_type.__name__
        result.label = titleize(result.name)  # TODO: Add override from settings
        result.comment = record_type.__doc__ or ""  # TODO: Revise

        # Set type kind by detecting the presence of 'get_key' method to indicate a record vs. an element
        is_record = hasattr(record_type, "get_key")
        is_abstract = hasattr(record_type, "__abstractmethods__") and bool(record_type.__abstractmethods__)
        if is_record:
            result.kind = TypeKind.Abstract if is_abstract else None
        else:
            result.kind = TypeKind.AbstractElement if is_abstract else TypeKind.Element

        # Set display kind
        result.display_kind = DisplayKind.Basic  # TODO: Add the ability to set display_kind

        # Set parent class as the first class in MRO that is not self and does not have Mixin suffix
        for parent_type in record_type.__mro__:
            if parent_type is not record_type and not parent_type.__name__.endswith("Mixin"):
                parent_type_module = ModuleDecl, parent_type.__module__
                parent_type_name = parent_type.__name__
                result.inherit = TypeDecl, parent_type_module, parent_type_name

        # Get key fields by parsing the source of 'get_key' method
        result.keys = KeyUtil.get_key_fields(record_type)

        # Use this flag to skip fields generation when the method is invoked from a derived class
        if not skip_fields:
            # Get type hints to resolve ForwardRefs
            type_hints = get_type_hints(record_type)

            # Add an element for each type hint
            result.elements = []
            for field_name, field_type in type_hints.items():
                # Get the rest of the data from the field itself
                field_decl = FieldDecl.create(field_name, field_type)

                # Convert to element and add
                element_decl = ElementDecl.create(field_decl)
                result.elements.append(element_decl)

        return result
