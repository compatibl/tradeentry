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

from cl.runtime.core.schema.decl.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.core.schema.decl.handler_implement_block_decl import HandlerImplementBlockDecl
from cl.runtime.core.schema.decl.interface_decl_key import InterfaceDeclKey
from cl.runtime.core.schema.decl.type_argument_decl import TypeArgumentDecl
from cl.runtime.core.schema.decl.type_decl_key import TypeDeclKey
from cl.runtime.core.schema.decl.type_element_decl import TypeElementDecl
from cl.runtime.core.schema.decl.type_index_decl import TypeIndexDecl
from cl.runtime.core.schema.decl.type_kind import TypeKind
from cl.runtime.core.schema.decl.type_param_decl import TypeParamDecl
from cl.runtime.core.storage.class_field import class_field
from cl.runtime.core.storage.class_label import class_label


@class_label('Type Declaration')
@dataclass
class TypeDecl(TypeDeclKey):
    """
    Defines type declaration. A tag of entity type XML representation corresponds to each element of the type. The
    names of type elements and corresponding tags coincide.
    """

    label: str = class_field()
    """Type label."""

    comment: Optional[str] = class_field()
    """Type comment. Contains additional information."""

    category: Optional[str] = class_field()
    """Category."""

    shortcut: Optional[str] = class_field()
    """Shortcut."""

    type_params: Optional[List[TypeParamDecl]] = class_field()
    """Type Params"""

    aliases: Optional[List[str]] = class_field()
    """Type aliases."""

    kind: Optional[TypeKind] = class_field()
    """Type kind."""

    inherit: Optional[TypeDeclKey] = class_field()
    """Parent type reference."""

    inherit_type_arguments: Optional[List[TypeArgumentDecl]] = class_field()
    """Inherit Type Argument."""

    interfaces: Optional[List[InterfaceDeclKey]] = class_field()
    """Parent interfaces"""

    declare: Optional[HandlerDeclareBlockDecl] = class_field()
    """Handler declaration block."""

    implement: Optional[HandlerImplementBlockDecl] = class_field()
    """Handler implementation block."""

    elements: Optional[List[TypeElementDecl]] = class_field()
    """Element declaration block."""

    keys: Optional[List[str]] = class_field()
    """Array of key element names."""

    indexes: Optional[List[TypeIndexDecl]] = class_field()
    """Defines indexes for the type."""

    immutable: Optional[bool] = class_field()
    """Immutable flag."""

    ui_response: Optional[bool] = class_field()
    """Flag indicating UiResponse."""

    seed: Optional[int] = class_field()
    """Seed."""

    version: Optional[str] = class_field()
    """Type Version"""

    system: Optional[bool] = class_field()
    """System."""

    enable_cache: Optional[bool] = class_field()
    """Enable cache flag."""

    partial: Optional[bool] = class_field()
    """It is possible to split the code over two or more source files."""

    abstract: Optional[bool] = class_field()
    """
    Abstract flag: is a restricted type that cannot be used to create objects (to access it, it must be inherited from
    another type).
    """

    interactive_edit: Optional[bool] = class_field()
    """Interactive Edit"""

    permanent: Optional[bool] = class_field()
    """Save records always permanently."""

    pinned: Optional[bool] = class_field()
    """Store records always in root dataset."""
