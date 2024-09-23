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

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from cl.convince.llms.completion_cache import CompletionCache
from cl.runtime.records.record_mixin import RecordMixin
from cl.convince.llms.llm_key import LlmKey


@dataclass(slots=True, kw_only=True)
class Llm(LlmKey, RecordMixin[LlmKey], ABC):
    """Provides an API for single query and chat completion."""

    _completion_cache: CompletionCache | None = None
    """Completion cache is used to return cached LLM responses."""

    def get_key(self) -> LlmKey:
        return LlmKey(llm_id=self.llm_id)

    def completion(self, query: str) -> str:
        """Text-in, text-out single query completion without model-specific tags (uses response caching)."""

        # Create completion cache if does not exist
        if self._completion_cache is None:
            self._completion_cache = CompletionCache(channel=self.llm_id)

        # Try to find in completion cache
        if (result := self._completion_cache.get(query)) is not None:
            # Return cached value if found
            return result
        else:
            # Otherwise make cloud provider call
            result = self.uncached_completion(query)
            # Save the result in cache before returning
            self._completion_cache.add(query, result)
            return result

    @abstractmethod
    def uncached_completion(self, query: str) -> str:
        """Perform completion without CompletionCache lookup, call completion instead."""


