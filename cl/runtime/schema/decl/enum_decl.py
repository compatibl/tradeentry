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

from cl.runtime.schema.decl.enum_decl_key import EnumDeclKey
from cl.runtime.schema.decl.enum_item_decl import EnumItemDecl
from dataclasses import dataclass
from cl.runtime.classes.dataclasses.dataclass_fields import data_field
from cl.runtime.classes.record_mixin import RecordMixin
from typing import List
from typing import Optional


@dataclass
class EnumDecl(EnumDeclKey, RecordMixin):
    """Enum declaration."""

    label: str = data_field()
    """Enum label."""

    comment: Optional[str] = data_field()
    """Enum comment."""

    items: List[EnumItemDecl] = data_field()
    """Array of enum items."""
