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

from typing import TYPE_CHECKING, List, Optional

from dataclasses import dataclass

from cl.runtime.core.storage.class_label import class_label
from cl.runtime.core.schema.v1.enum_decl_key import EnumDeclKey
from cl.runtime.core.schema.v1.interface_decl_key import InterfaceDeclKey
from cl.runtime.core.schema.v1.type_decl_key import TypeDeclKey
from cl.runtime.core.schema.v1.value_decl import ValueDecl
from cl.runtime.core.storage.class_data import ClassData, class_field

if TYPE_CHECKING:
    from cl.runtime.core.schema.v1.type_argument_decl import TypeArgumentDecl


@class_label('Type Member Declaration')
@dataclass
class TypeMemberDecl(ClassData):
    """Type member declaration."""

    type_param: Optional[str] = class_field()
    """Type Param"""

    value: Optional[ValueDecl] = class_field()
    """Value or atomic element declaration."""

    enum: Optional[EnumDeclKey] = class_field()
    """Enumeration element declaration."""

    data: Optional[TypeDeclKey] = class_field()
    """Data element declaration."""

    key_: Optional[TypeDeclKey] = class_field(name='Key')
    """Key element declaration."""

    query: Optional[TypeDeclKey] = class_field()
    """Query element declaration."""

    condition: Optional[TypeDeclKey] = class_field()
    """Condition element declaration."""

    type_arguments: Optional[List['TypeArgumentDecl']] = class_field()
    """Type Argument."""

    interface: Optional[InterfaceDeclKey] = class_field()
    """Interface element declaration."""

    handler_args: Optional[TypeDeclKey] = class_field()
    """HandlerArgs element declaration."""
