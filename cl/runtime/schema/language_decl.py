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

from typing import final
from cl.runtime.records.dataclasses.dataclass_mixin import datafield, DataclassMixin
from cl.runtime.schema.language_key import LanguageKey


@final
class Language(DataclassMixin):
    """Implementation language for a handler or viewer."""

    language_id: str = datafield(name='LanguageID')
    """Language."""

    language_label: str | None = datafield()
    """Language label displayed in user interface (may not be unique)."""

    def get_key(self) -> LanguageKey:
        return type(self), self.language_id
