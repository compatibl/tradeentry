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

import ast
import inspect
import textwrap
from dataclasses import dataclass
from enum import Enum

from inflection import titleize
from typing import List
from typing import get_type_hints, Type
from typing_extensions import Self
from cl.runtime.records.dataclasses.dataclass_mixin import DataclassMixin
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.schema.display_kind import DisplayKind
from cl.runtime.schema.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.schema.module_decl import ModuleDecl
from cl.runtime.schema.module_decl_key import ModuleDeclKey
from cl.runtime.schema.type_decl_key import TypeDeclKey
from cl.runtime.schema.element_decl import ElementDecl
from cl.runtime.schema.type_index_decl import TypeIndexDecl
from cl.runtime.schema.type_kind import TypeKind


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
        return type(self), self.module, self.name

    @classmethod
    def _create_partial(cls, record_type: Type) -> Self:
        """Create partial type declaration without elements for a dataclass_transform based class."""

        if issubclass(cls, Enum):
            raise RuntimeError(f"Cannot create TypeDecl for class {record_type.__name__}"
                               f"because it is an enum, create EnumDecl instead.")
        if issubclass(cls, tuple):
            raise RuntimeError(f"Cannot create TypeDecl for class {record_type.__name__} because it is a tuple.")

        # Create instance of the final type
        result = cls()

        result.module = ModuleDecl, record_type.__module__
        result.name = record_type.__name__
        result.label = titleize(result.name)  # TODO: Add override from settings
        result.comment = record_type.__doc__ or ""  # TODO: Revise

        # Set type kind by detecting the presence of 'get_key' method to indicate a record vs. an element
        is_record = hasattr(record_type, 'get_key')
        is_abstract = hasattr(record_type, '__abstractmethods__') and bool(record_type.__abstractmethods__)
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
        result.keys = cls._get_key_fields(record_type)

        return result

    @classmethod
    def _get_key_fields(cls, record_type: Type) -> List[str]:
        """
        Get key fields by parsing the source of 'get_key' method.

        Notes:
            This method parses the source code of 'get_key' method and returns all instance
            fields it accesses in the order of access, for example if 'get_key' source is:

            def get_key(self) -> Tuple[Type, str, int]:
                return ClassName, self.key_field_1, self.key_field_2

            this method will return:

            ["key_field_1", "key_field_2"]
        """

        # Get source code for the 'get_key' method
        if hasattr(record_type, "get_key"):
            get_key_source = inspect.getsource(record_type.get_key)
        else:
            raise RuntimeError(
                f"Cannot get key fields because {record_type.__name__} " f"does not implement 'get_key' method."
            )

        # Because 'ast' expects the code to be correct as though it is at top level,
        # remove excess indent from the source to make it suitable for parsing
        get_key_source = textwrap.dedent(get_key_source)

        # Extract field names from the AST of 'get_key' method
        get_key_ast = ast.parse(get_key_source)
        key_fields = []
        for node in ast.walk(get_key_ast):
            # Find every instance field of 'cls' accessed inside the source of 'get_key' method.
            # Accumulate in list in the order they are accessed
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":
                key_fields.append(node.attr)

        return key_fields
