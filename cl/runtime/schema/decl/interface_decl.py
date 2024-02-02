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
from cl.runtime.schema.decl.handler_declare_decl import HandlerDeclareDecl
from cl.runtime.schema.decl.interface_decl_key import InterfaceDeclKey
from cl.runtime.schema.decl.type_element_decl import TypeElementDecl


@attrs_record
class InterfaceDecl(InterfaceDeclKey, Record):
    """Defines Interface declaration."""

    label: str = attrs_field()
    """Type label."""

    comment: Optional[str] = attrs_field()
    """Type comment. Contains additional information."""

    aliases: Optional[List[str]] = attrs_field()
    """Interface aliases."""

    interfaces: Optional[List[InterfaceDeclKey]] = attrs_field()
    """Parent interfaces"""

    handlers: Optional[List[HandlerDeclareDecl]] = attrs_field()
    """Handler declaration data."""

    elements: Optional[List[TypeElementDecl]] = attrs_field()
    """Element declaration block."""

    attributes: Optional[List[TypeElementDecl]] = attrs_field()
    """Attribute declaration block."""
