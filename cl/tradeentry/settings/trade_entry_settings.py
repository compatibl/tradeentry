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
from cl.runtime.settings.settings import Settings


@dataclass(slots=True, kw_only=True)
class TradeEntrySettings(Settings):
    """Settings that apply to the entire TradeEntry package."""

    mini_llm: str
    """String identifier of the default mini LLM used for simpler tasks by the tradeentry package."""

    full_llm: str
    """String identifier of the full mini LLM used for more complex tasks by the tradeentry package."""

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""

        if not isinstance(self.mini_llm, str):
            raise RuntimeError(f"{type(self).__name__} field 'mini_llm' must be a string.")
        if not isinstance(self.full_llm, str):
            raise RuntimeError(f"{type(self).__name__} field 'full_llm' must be a string.")

    @classmethod
    def get_prefix(cls) -> str:
        return "tradeentry"
