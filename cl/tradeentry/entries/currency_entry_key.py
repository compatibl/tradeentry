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

from dataclasses import dataclass
from typing import Type
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin


@dataclass(slots=True, kw_only=True)
class CurrencyEntryKey(KeyMixin):
    """Maps currency string specified by the user to the ISO-4217 three-letter currency code."""

    entry_id: str = missing()
    """Currency entry string specified by the user (may not be the ISO-4217 three-letter currency code)."""

    @classmethod
    def get_key_type(cls) -> Type:
        return CurrencyEntryKey
