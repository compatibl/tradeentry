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

from cl.runtime.records.dataclasses.dataclass_record_mixin import DataclassRecordMixin
from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield
from cl.runtime.schema.enum_decl_key import EnumDeclKey
from cl.runtime.schema.enum_item_decl import EnumItemDecl
from dataclasses import dataclass
from typing import List


@dataclass(slots=True, kw_only=True)
class EnumDecl(EnumDeclKey, DataclassRecordMixin):
    """Enum declaration."""

    label: str | None = datafield()
    """Enum label."""

    comment: str | None = datafield()
    """Enum comment."""

    items: List[EnumItemDecl] = datafield()
    """Array of enum items."""

    def get_key(self) -> EnumDeclKey:
        return EnumDeclKey(module=self.module, name=self.name)

