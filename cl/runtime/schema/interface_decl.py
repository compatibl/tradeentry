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
from cl.runtime.schema.handler_declare_decl import HandlerDeclareDecl
from cl.runtime.schema.interface_decl_key import InterfaceDeclKey
from cl.runtime.schema.module_decl_key import ModuleDeclKey
from cl.runtime.schema.type_element_decl import TypeElementDecl
from cl.runtime.records.dataclasses.dataclass_mixin import datafield, DataclassMixin


class InterfaceDecl(DataclassMixin):
    """Defines Interface declaration."""

    module: ModuleDeclKey = datafield()
    """Module reference."""

    name: str = datafield()
    """Type name is unique when combined with module."""

    label: str = datafield()
    """Type label."""

    comment: str | None = datafield()
    """Type comment. Contains additional information."""

    aliases: List[str] | None = datafield()
    """Interface aliases."""

    interfaces: Optional[List[InterfaceDeclKey]] = datafield()
    """Parent interfaces"""

    handlers: Optional[List[HandlerDeclareDecl]] = datafield()
    """Handler declaration data."""

    elements: Optional[List[TypeElementDecl]] = datafield()
    """Element declaration block."""

    attributes: Optional[List[TypeElementDecl]] = datafield()
    """Attribute declaration block."""

    def get_key(self) -> InterfaceDeclKey:
        return type(self), self.module, self.name
