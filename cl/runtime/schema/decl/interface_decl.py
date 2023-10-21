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

from cl.runtime.schema.decl.handler_declare_decl import HandlerDeclareDecl
from cl.runtime.schema.decl.interface_decl_key import InterfaceDeclKey
from cl.runtime.schema.decl.type_element_decl import TypeElementDecl
from cl.runtime.storage.class_field import class_field
from cl.runtime.storage.class_label import class_label


@class_label('Interface Declaration')
@dataclass
class InterfaceDecl(InterfaceDeclKey):
    """Defines Interface declaration."""

    label: str = class_field()
    """Type label."""

    comment: Optional[str] = class_field()
    """Type comment. Contains additional information."""

    aliases: Optional[List[str]] = class_field()
    """Interface aliases."""

    interfaces: Optional[List[InterfaceDeclKey]] = class_field()
    """Parent interfaces"""

    handlers: Optional[List[HandlerDeclareDecl]] = class_field()
    """Handler declaration data."""

    elements: Optional[List[TypeElementDecl]] = class_field()
    """Element declaration block."""

    attributes: Optional[List[TypeElementDecl]] = class_field()
    """Attribute declaration block."""
