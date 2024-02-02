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

from cl.runtime.storage.attrs_data_util import attrs_data
from cl.runtime.storage.attrs_field_util import attrs_field
from typing import TYPE_CHECKING, List, Optional

from cl.runtime.schema.decl.enum_decl_key import EnumDeclKey
from cl.runtime.schema.decl.interface_decl_key import InterfaceDeclKey
from cl.runtime.schema.decl.type_decl_key import TypeDeclKey
from cl.runtime.schema.decl.value_decl import ValueDecl
from cl.runtime.storage.data import Data

if TYPE_CHECKING:
    from cl.runtime.schema.decl.type_argument_decl import TypeArgumentDecl


@attrs_data
class TypeMemberDecl(Data):
    """Type member declaration."""

    type_param: Optional[str] = attrs_field()
    """Type Param"""

    value: Optional[ValueDecl] = attrs_field()
    """Value or atomic element declaration."""

    enum: Optional[EnumDeclKey] = attrs_field()
    """Enumeration element declaration."""

    data: Optional[TypeDeclKey] = attrs_field()
    """Data element declaration."""

    key_: Optional[TypeDeclKey] = attrs_field(name='Key')
    """Key element declaration."""

    query: Optional[TypeDeclKey] = attrs_field()
    """Query element declaration."""

    condition: Optional[TypeDeclKey] = attrs_field()
    """Condition element declaration."""

    type_arguments: Optional[List['TypeArgumentDecl']] = attrs_field()
    """Type Argument."""

    interface: Optional[InterfaceDeclKey] = attrs_field()
    """Interface element declaration."""

    handler_args: Optional[TypeDeclKey] = attrs_field()
    """HandlerArgs element declaration."""
