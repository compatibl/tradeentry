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

from typing import Optional, final

from cl.runtime import Record
from cl.runtime.decorators.attrs_record_decorator import attrs_record
from cl.runtime.schema.decl.language_key import LanguageKey
from cl.runtime.decorators.data_field_decorator import data_field


@final
@attrs_record
class Language(LanguageKey, Record):
    language_label: Optional[str] = data_field()
    """Language label displayed in user interface (may not be unique)."""
