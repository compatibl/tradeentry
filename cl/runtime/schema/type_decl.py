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

from dataclasses import dataclass
from typing import List, Optional

from cl.runtime.schema.display_kind import DisplayKind
from cl.runtime.schema.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.schema.handler_implement_block_decl import HandlerImplementBlockDecl
from cl.runtime.schema.interface_decl_key import InterfaceDeclKey
from cl.runtime.schema.module_decl_key import ModuleDeclKey
from cl.runtime.schema.type_decl_key import TypeDeclKey
from cl.runtime.schema.type_element_decl import TypeElementDecl
from cl.runtime.schema.type_index_decl import TypeIndexDecl
from cl.runtime.schema.type_kind import TypeKind
from cl.runtime.schema.type_param_decl import TypeParamDecl
from dataclasses import dataclass
from cl.runtime.records.dataclasses.dataclass_mixin import datafield, DataclassMixin


@dataclass(slots=True)
class TypeDecl(DataclassMixin):
    """
    Defines type declaration. A tag of entity type XML representation corresponds to each element of the type. The
    names of type elements and corresponding tags coincide.
    """

    module: ModuleDeclKey = datafield()
    """Module reference."""

    name: str = datafield()
    """Type name is unique when combined with module."""

    label: str = datafield()
    """Type label."""

    comment: str | None = datafield()
    """Type comment. Contains additional information."""

    shortcut: str | None = datafield()
    """Shortcut."""

    type_params: Optional[List[TypeParamDecl]] = datafield()
    """Type Params"""

    aliases: List[str] | None = datafield()
    """Type aliases."""

    kind: Optional[TypeKind] = datafield()
    """Type kind."""

    display_kind: Optional[DisplayKind] = datafield()
    """Display kind."""

    inherit: Optional[TypeDeclKey] = datafield()
    """Parent type reference."""

    interfaces: Optional[List[InterfaceDeclKey]] = datafield()
    """Parent interfaces"""

    declare: Optional[HandlerDeclareBlockDecl] = datafield()
    """Handler declaration block."""

    implement: Optional[HandlerImplementBlockDecl] = datafield()
    """Handler implementation block."""

    elements: Optional[List[TypeElementDecl]] = datafield()
    """Element declaration block."""

    keys: List[str] | None = datafield()
    """Array of key element names."""

    indexes: Optional[List[TypeIndexDecl]] = datafield()
    """Defines indexes for the type."""

    immutable: Optional[bool] = datafield()
    """Immutable flag."""

    ui_response: Optional[bool] = datafield()
    """Flag indicating UiResponse."""

    seed: Optional[int] = datafield()
    """Seed."""

    version: str | None = datafield()
    """Type Version"""

    system: Optional[bool] = datafield()
    """System."""

    enable_cache: Optional[bool] = datafield()
    """Enable cache flag."""

    partial: Optional[bool] = datafield()
    """It is possible to split the code over two or more source files."""

    abstract: Optional[bool] = datafield()
    """
    Abstract flag: is a restricted type that cannot be used to create objects (to access it, it must be inherited from
    another type).
    """

    hidden: Optional[bool] = datafield()
    """Enable Hidden flag."""

    permanent: Optional[bool] = datafield()
    """Save records always permanently."""

    def get_key(self) -> TypeDeclKey:
        return type(self), self.module, self.name
