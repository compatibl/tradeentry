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

from cl.runtime.schema.index_decl import IndexDecl
from dataclasses import dataclass
from cl.runtime.records.dataclasses.dataclass_mixin import datafield


@dataclass(slots=True)
class TypeIndexDecl:
    """Type index declaration."""

    name: str | None = datafield()
    """Index name."""

    elements: List[IndexDecl] = datafield()
    """Index elements."""

    ignore_system_fields: Optional[bool] = datafield()
    """Flag indicating if index should include system fields."""
