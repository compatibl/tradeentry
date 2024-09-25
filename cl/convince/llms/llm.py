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
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.records.record_mixin import RecordMixin
from cl.convince.llms.completion_cache import CompletionCache
from cl.convince.llms.llm_key import LlmKey


@dataclass(slots=True, kw_only=True)
class Llm(LlmKey, RecordMixin[LlmKey], ABC):
    """Provides an API for single query and chat completion."""

    _completion_cache: CompletionCache | None = None
    """Completion cache is used to return cached LLM responses."""

    def get_key(self) -> LlmKey:
        return LlmKey(llm_id=self.llm_id)

    def completion(self, query: str, *, trial_id: str | int | None = None) -> str:
        """Text-in, text-out single query completion without model-specific tags (uses response caching)."""

        # Normalize EOL character and remove leading and trailing whitespace in query
        query = CompletionCache.normalize_value(query)

        # Create completion cache if does not exist
        if self._completion_cache is None:
            self._completion_cache = CompletionCache(channel=self.llm_id)

        # Try to find in completion cache by cache_key, make cloud provider call only if not found
        if (result := self._completion_cache.get(query, trial_id=trial_id)) is None:
            # Generate OrderedUuid and convert to readable ordered string in date-hash format
            request_uuid = OrderedUuid.create_one()
            request_id = OrderedUuid.to_readable_str(request_uuid)

            # Invoke LLM by calling the cloud provider API
            result = self.uncached_completion(request_id, query)

            # Save the result in cache before returning, request_id is recorded
            # but not taken into account during lookup
            self._completion_cache.add(request_id, query, result, trial_id=trial_id)

        # Normalize EOL character and remove leading and trailing whitespace in result
        result = CompletionCache.normalize_value(result)
        return result

    @abstractmethod
    def uncached_completion(self, request_id: str, query: str) -> str:
        """Perform completion without CompletionCache lookup, call completion instead."""
