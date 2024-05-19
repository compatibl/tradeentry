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

from cl.runtime.schema.dict_decl import DictDecl
from cl.runtime.schema.enum_decl_key import EnumDeclKey
from cl.runtime.schema.interface_decl_key import InterfaceDeclKey
from cl.runtime.schema.type_decl_key import TypeDeclKey
from cl.runtime.schema.value_decl import ValueDecl
from dataclasses import dataclass
from cl.runtime.records.dataclasses.dataclass_mixin import datafield

if TYPE_CHECKING:
    from cl.runtime.schema.type_argument_decl import TypeArgumentDecl


@dataclass(slots=True)
class TypeMemberDecl:
    """Type member declaration."""

    type_param: str | None = datafield()
    """Type Param"""

    value: Optional[ValueDecl] = datafield()
    """Value or atomic element declaration."""

    enum: Optional[EnumDeclKey] = datafield()
    """Enumeration element declaration."""

    data: Optional[TypeDeclKey] = datafield()
    """Data element declaration."""

    key_: Optional[TypeDeclKey] = datafield(name='Key')
    """Key element declaration."""

    query: Optional[TypeDeclKey] = datafield()
    """Query element declaration."""

    condition: Optional[TypeDeclKey] = datafield()
    """Condition element declaration."""

    type_arguments: Optional[List['TypeArgumentDecl']] = datafield()
    """Type Argument."""

    interface: Optional[InterfaceDeclKey] = datafield()
    """Interface element declaration."""

    handler_args: Optional[TypeDeclKey] = datafield()
    """HandlerArgs element declaration."""

    dict: Optional[DictDecl] = datafield()
    """Enumeration element declaration."""
