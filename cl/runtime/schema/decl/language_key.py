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

from cl.runtime.classes.attrs_util import data_class
from cl.runtime.classes.attrs_util import data_field
from cl.runtime.classes.key_mixin import KeyMixin


@data_class
class LanguageKey(KeyMixin):
    language_id: str = data_field(name="LanguageID")
    """Language."""

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return self.language_id
