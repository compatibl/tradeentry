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

from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.schema.member_decl import MemberDecl
from dataclasses import dataclass
from typing import List
from typing import Optional


@dataclass(slots=True, kw_only=True)
class ElementDecl(MemberDecl):  # TODO: Consider renaming to TypeFieldDecl or FieldDecl
    """Type element declaration."""

    name: str = datafield()
    """Element name."""

    label: str | None = datafield()
    """Element label. If not specified, name is used instead."""

    comment: str | None = datafield()
    """Element comment. Contains addition information."""

    vector: Optional[bool] = datafield()  # TODO: Replace by container field with enum values vector/array, dict, DF
    """Flag indicating variable size array (vector) container."""

    optional: Optional[bool] = datafield()
    """Flag indicating optional element."""

    optional_vector_element: Optional[bool] = datafield()  # TODO: Rename to optional_element or optional_field
    """Flag indicating optional vector item element."""

    additive: Optional[bool] = datafield()
    """Optional flag indicating if the element is additive and that the total column can be shown in the UI."""

    format_: str | None = datafield(name="Format")  # TODO: Use Python interpolated string format
    """Specifies UI Format for the element."""

    alternate_of: str | None = datafield()
    """Link current element to AlternateOf element. In the editor these elements will be treated as a choice."""

