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

from cl.runtime.classes.attrs import data_class
from cl.runtime.classes.attrs import data_field
from cl.runtime.classes.key_mixin import KeyMixin
from typing import Optional


@data_class
class ModuleKey(KeyMixin):
    """
    Defines Analyst module.
    Module can be represented both as the source code and precomiled dll (defined by flag "Compiled").
    """

    module_name: Optional[str] = data_field()
    """Unique module identifier in dot delimited format."""

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return self.module_name
