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

from cl.runtime.schema.element_modification_type import ElementModificationType
from cl.runtime.schema.type_member_decl import TypeMemberDecl
from cl.runtime.records.dataclasses.dataclass_mixin import datafield


class TypeElementDecl(TypeMemberDecl):
    """Type element declaration."""

    name: str = datafield()
    """Element name."""

    label: str | None = datafield()
    """Element label. If not specified, name is used instead."""

    comment: str | None = datafield()
    """Element comment. Contains addition information."""

    vector: Optional[bool] = datafield()
    """Flag indicating variable size array (vector) container."""

    aliases: List[str] | None = datafield()
    """Element aliases."""

    optional: Optional[bool] = datafield()
    """Flag indicating optional element."""

    optional_vector_element: Optional[bool] = datafield()
    """Flag indicating optional vector item element."""

    secure: Optional[bool] = datafield()
    """Secure flag."""

    filterable: Optional[bool] = datafield()
    """Flag indicating filterable element."""

    read_only: Optional[bool] = datafield()
    """Flag indicating readonly element."""

    hidden: Optional[bool] = datafield()
    """Flag indicating a hidden element. Hidden elements are visible in API but not in the UI."""

    additive: Optional[bool] = datafield()
    """Optional flag indicating if the element is additive and that the total column can be shown in the UI."""

    format_: str | None = datafield(name='Format')
    """Specifies UI Format for the element."""

    output: Optional[bool] = datafield()
    """Flag indicating output element. These elements will be readonly in UI and can be fulfilled by handlers."""

    alternate_of: str | None = datafield()
    """Link current element to AlternateOf element. In the editor these elements will be treated as a choice."""

    viewer: str | None = datafield()
    """The element will be viewed under specified tab."""

    modification_type: Optional[ElementModificationType] = datafield()
    """Element Modification Type."""
