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

from cl.runtime.data.attrs.attrs_data_util import attrs_data
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from typing import Optional

from cl.runtime.schema.decl.type_decl_key import TypeDeclKey
from cl.runtime.schema.decl.type_member_decl import TypeMemberDecl


@attrs_data
class HandlerVariableDecl(TypeMemberDecl):
    """Handler parameter or return variable declaration."""

    vector: Optional[bool] = attrs_field()
    """Flag indicating variable size array (vector) container."""

    object_: Optional[TypeDeclKey] = attrs_field(name='Object')
    """Object element declaration."""

    optional: Optional[bool] = attrs_field()
    """Flag indicating optional element."""

    hidden: Optional[bool] = attrs_field()
    """Flag indicating a hidden element. Hidden elements are visible in API but not in the UI."""

    label: Optional[str] = attrs_field()
    """Parameter label."""

    comment: Optional[str] = attrs_field()
    """Parameter comment. Contains addition information about handler parameter."""
