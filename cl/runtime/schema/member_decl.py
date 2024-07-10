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

from cl.runtime.records.dataclasses_extensions import datafield
from cl.runtime.schema.enum_decl_key import EnumDeclKey
from cl.runtime.schema.type_decl_key import TypeDeclKey
from cl.runtime.schema.value_decl import ValueDecl
from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class MemberDecl:
    """Type member declaration."""

    value: ValueDecl | None = datafield()  # TODO: Flatten value and other types to a single field
    """Value or primitive element declaration."""

    enum: EnumDeclKey | None = datafield()
    """Enumeration element declaration."""

    data: TypeDeclKey | None = datafield()
    """Data element declaration."""

    key_: TypeDeclKey | None = datafield(name="Key")  # TODO: Remove trailing _ automatically instead
    """Key element declaration."""

    query: TypeDeclKey | None = datafield()
    """Query element declaration."""

    condition: TypeDeclKey | None = datafield()
    """Condition element declaration."""
