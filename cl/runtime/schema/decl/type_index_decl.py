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
from cl.runtime.storage.attrs import attrs_field, attrs_class
from typing import List, Optional

from cl.runtime.schema.decl.index_decl import IndexDecl
from cl.runtime.storage.data import Data


@attrs_data
class TypeIndexDecl(Data):
    """Type index declaration."""

    name: Optional[str] = attrs_field()
    """Index name."""

    elements: List[IndexDecl] = attrs_field()
    """Index elements."""
