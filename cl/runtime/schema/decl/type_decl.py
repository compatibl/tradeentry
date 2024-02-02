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

from typing import List, Optional
from cl.runtime.storage.record import Record
from cl.runtime.storage.attrs_record_util import attrs_record
from cl.runtime.storage.attrs_field_util import attrs_field
from cl.runtime.schema.decl.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.schema.decl.handler_implement_block_decl import HandlerImplementBlockDecl
from cl.runtime.schema.decl.interface_decl_key import InterfaceDeclKey
from cl.runtime.schema.decl.type_argument_decl import TypeArgumentDecl
from cl.runtime.schema.decl.type_decl_key import TypeDeclKey
from cl.runtime.schema.decl.type_element_decl import TypeElementDecl
from cl.runtime.schema.decl.type_index_decl import TypeIndexDecl
from cl.runtime.schema.decl.type_kind import TypeKind
from cl.runtime.schema.decl.type_param_decl import TypeParamDecl


@attrs_record
class TypeDecl(TypeDeclKey, Record):
    """
    Defines type declaration. A tag of entity type XML representation corresponds to each element of the type. The
    names of type elements and corresponding tags coincide.
    """

    label: str = attrs_field()
    """Type label."""

    comment: Optional[str] = attrs_field()
    """Type comment. Contains additional information."""

    category: Optional[str] = attrs_field()
    """Category."""

    shortcut: Optional[str] = attrs_field()
    """Shortcut."""

    type_params: Optional[List[TypeParamDecl]] = attrs_field()
    """Type Params"""

    aliases: Optional[List[str]] = attrs_field()
    """Type aliases."""

    kind: Optional[TypeKind] = attrs_field()
    """Type kind."""

    inherit: Optional[TypeDeclKey] = attrs_field()
    """Parent type reference."""

    inherit_type_arguments: Optional[List[TypeArgumentDecl]] = attrs_field()
    """Inherit Type Argument."""

    interfaces: Optional[List[InterfaceDeclKey]] = attrs_field()
    """Parent interfaces"""

    declare: Optional[HandlerDeclareBlockDecl] = attrs_field()
    """Handler declaration block."""

    implement: Optional[HandlerImplementBlockDecl] = attrs_field()
    """Handler implementation block."""

    elements: Optional[List[TypeElementDecl]] = attrs_field()
    """Element declaration block."""

    keys: Optional[List[str]] = attrs_field()
    """Array of key element names."""

    indexes: Optional[List[TypeIndexDecl]] = attrs_field()
    """Defines indexes for the type."""

    immutable: Optional[bool] = attrs_field()
    """Immutable flag."""

    ui_response: Optional[bool] = attrs_field()
    """Flag indicating UiResponse."""

    seed: Optional[int] = attrs_field()
    """Seed."""

    version: Optional[str] = attrs_field()
    """Type Version"""

    system: Optional[bool] = attrs_field()
    """System."""

    enable_cache: Optional[bool] = attrs_field()
    """Enable cache flag."""

    partial: Optional[bool] = attrs_field()
    """It is possible to split the code over two or more source files."""

    abstract: Optional[bool] = attrs_field()
    """
    Abstract flag: is a restricted type that cannot be used to create objects (to access it, it must be inherited from
    another type).
    """

    interactive_edit: Optional[bool] = attrs_field()
    """Interactive Edit"""

    permanent: Optional[bool] = attrs_field()
    """Save records always permanently."""

    pinned: Optional[bool] = attrs_field()
    """Store records always in root dataset."""
