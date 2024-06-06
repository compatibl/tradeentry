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

from cl.runtime.records.dataclasses.dataclass_mixin import DataclassMixin
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.schema.display_kind import DisplayKind
from cl.runtime.schema.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.schema.module_decl_key import ModuleDeclKey
from cl.runtime.schema.type_decl_key import TypeDeclKey
from cl.runtime.schema.element_decl import ElementDecl
from cl.runtime.schema.type_index_decl import TypeIndexDecl
from cl.runtime.schema.type_kind import TypeKind
from dataclasses import dataclass
from typing import List


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
