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
from typing import ClassVar
from anthropic import Anthropic
from cl.convince.llms.llm import Llm
from cl.convince.settings.anthropic_settings import AnthropicSettings
from cl.runtime.context.context_util import ContextUtil
from cl.runtime.log.exceptions.user_error import UserError


@dataclass(slots=True, kw_only=True)
class ClaudeLlm(Llm):
    """Implements Claude LLM API."""

    model_name: str | None = None
    """Model name in Anthropic format including version if any, defaults to 'llm_id'."""

    max_tokens: int = 4096
    """Maximum number of tokens the model will generate in response to the query."""

    _client: ClassVar[Anthropic] = None
    """Anthropic client instance."""

    def uncached_completion(self, request_id: str, query: str) -> str:
        """Perform completion without CompletionCache lookup, call completion instead."""

        # Prefix a unique RequestID to the model for audit log purposes and
        # to stop model provider from caching the results
        query_with_request_id = f"RequestID: {request_id}\n\n{query}"

        model_name = self.model_name if self.model_name is not None else self.llm_id
        messages = [{"role": "user", "content": query_with_request_id}]
        client = self._get_client()
        response = client.messages.create(
            model=model_name,
            messages=messages,
            max_tokens=self.max_tokens,
        )
        if len(response.content) != 1:
            raise RuntimeError(f"More than one response message received for query: {query}: {str(response)}")
        result = response.content[0].text
        return result

    @classmethod
    def _get_client(cls) -> Anthropic:
        """Instantiate and cache the Anthropic client instance."""

        # Try loading API key from context.secrets first and then from settings
        api_key = ContextUtil.get_secret("ANTHROPIC_API_KEY") or AnthropicSettings.instance().api_key
        if api_key is None:
            raise UserError("Provide ANTHROPIC_API_KEY in Account > My Keys (users) or using Dynaconf (developers).")

        if cls._client is None:
            cls._client = Anthropic(
                api_key=api_key,
            )
        return cls._client
