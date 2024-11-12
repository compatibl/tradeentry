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
from openai import OpenAI
from cl.runtime.context.context_util import ContextUtil
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.float_util import FloatUtil
from cl.convince.llms.llm import Llm
from cl.convince.settings.openai_settings import OpenaiSettings


@dataclass(slots=True, kw_only=True)
class GptLlm(Llm):
    """Implements GPT LLM API."""

    model_name: str | None = None
    """Model name in OpenAI format including version if any (optional, defaults to 'llm_id' field of the base class)."""

    temperature: float | None = None
    """
    The sampling temperature between 0 and 1 (optional, passed as 'temperature' to OpenAI SDK).

    Notes:
        Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it
        more focused  and deterministic. If set to 0, the model will use log probability to automatically
        increase the temperature until certain thresholds are hit.
    """

    _client: ClassVar[OpenAI] = None
    """OpenAI client instance."""

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""

        if self.temperature is not None:
            if isinstance(self.temperature, float) or isinstance(self.temperature, int):
                self.temperature = float(self.temperature)
                # Compare with tolerance in case it is calculated by a formula
                if FloatUtil.less(self.temperature, 0.0) or FloatUtil.more(self.temperature, 1.0):
                    raise RuntimeError(
                        f"{type(self).__name__} field temperature={self.temperature} "
                        f"is outside the range from 0 to 1."
                    )
                # Ensure that roundoff error does not move it out of range
                self.temperature = min(max(self.temperature, 0.0), 1.0)
            else:
                raise RuntimeError(f"{type(self).__name__} field 'api_base_url' must be None or a number from 0 to 1")

    def uncached_completion(self, request_id: str, query: str) -> str:
        """Perform completion without CompletionCache lookup, call completion instead."""

        # Prefix a unique RequestID to the model for audit log purposes and
        # to stop model provider from caching the results
        query_with_request_id = f"RequestID: {request_id}\n\n{query}"

        model_name = self.model_name if self.model_name is not None else self.llm_id
        messages = [{"role": "user", "content": query_with_request_id}]

        client = self._get_client()
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=self.temperature,
        )

        result = response.choices[0].message.content
        return result

    @classmethod
    def _get_client(cls) -> OpenAI:
        """Instantiate and cache the OpenAI client instance."""
        if cls._client is None:

            # Try loading API key from context.secrets first and then from settings
            api_key = ContextUtil.decrypt_secret("OPENAI_API_KEY") or OpenaiSettings.instance().api_key
            if api_key is None:
                raise UserError("Provide OPENAI_API_KEY in Account > My Keys (users) or using Dynaconf (developers).")

            cls._client = OpenAI(
                api_key=api_key,
                base_url=OpenaiSettings.instance().api_base_url,
            )
        return cls._client
