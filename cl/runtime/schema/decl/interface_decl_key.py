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

from cl.runtime.storage.attrs_key_util import attrs_key
from cl.runtime.storage.attrs_field_util import attrs_field
from cl.runtime.schema.decl.module_key import ModuleKey
from cl.runtime.storage.key import Key


@attrs_key
class InterfaceDeclKey(Key):
    """Defines Interface declaration."""

    module: ModuleKey = attrs_field()
    """Module reference."""

    name: str = attrs_field()
    """Type name is unique when combined with module."""

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return f'{self.module};{self.name}'
