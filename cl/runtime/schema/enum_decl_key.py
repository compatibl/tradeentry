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

from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield
from cl.runtime.records.dataclasses.dataclass_key_mixin import DataclassKeyMixin
from cl.runtime.schema.module_decl_key import ModuleDeclKey
from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True)
class EnumDeclKey(DataclassKeyMixin):
    """Enum declaration."""

    module: ModuleDeclKey = datafield()  # TODO: Merge with name
    """Module reference."""

    name: str = datafield()
    """Enum name is unique when combined with module."""

    def get_generic_key(self) -> Tuple:
        return EnumDeclKey, self.module.get_generic_key(), self.name
