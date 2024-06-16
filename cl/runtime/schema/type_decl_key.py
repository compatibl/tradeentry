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

from __future__ import annotations
from typing import final
from typing import Tuple
from typing import Type

from cl.runtime.records.table_mixin import TableMixin
from cl.runtime.schema.module_decl_key import ModuleDeclKey, ModuleDeclTable


@final
class TypeDeclTable(TableMixin):
    """Table settings class."""

    @classmethod
    def create_key(cls, *, module: ModuleDeclKey | str, name: str) -> TypeDeclKey:
        if isinstance(module, tuple):
            return TypeDeclTable, module, name
        elif isinstance(module, str):
            return TypeDeclTable, ModuleDeclTable.create_key(module_name=module), name
        else:
            raise RuntimeError(f"Module {module} is neither a tuple nor a string.")


TypeDeclKey = Tuple[Type[TypeDeclTable], ModuleDeclKey, str]
