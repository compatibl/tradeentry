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
import google.generativeai as gemini  # noqa
from cl.convince.llms.llm import Llm
from cl.convince.settings.gemini_settings import GeminiSettings


@dataclass(slots=True, kw_only=True)
class GeminiLlm(Llm):
    """Implements Gemini LLM API."""

    model_name: str | None = None
    """Model name in Gemini format including version if any, defaults to 'llm_id'."""

    def uncached_completion(self, query: str) -> str:
        """Perform completion without CompletionCache lookup, call completion instead."""

        model_name = self.model_name if self.model_name is not None else self.llm_id

        gemini.configure(api_key=GeminiSettings.instance().api_key)
        model = gemini.GenerativeModel(model_name=model_name)
        response = model.generate_content(query)

        result = response.text
        return result

    @classmethod
    def create_prompt_from_messages(cls, messages: list[dict]) -> list[dict[str, str]]:
        """
        Having a list of messages in the following format:
        [
            {"role": "system", "content": "System Prompt"},
            {"role": "user", "content": "What is 2 + 2?"},
            {"role": "assistant", "content": "2+2 is equals to 4"},
            {"role": "user", "content": "Answer only with resulting number"},
        ]
        Returns:
        [
            {"role": "system", "parts": ["System Prompt"]},
            {"role": "user", "parts": ["What is 2 + 2?"]},
            {"role": "assistant", "parts": ["2+2 is equals to 4"]},
            {"role": "user", "parts": ["Answer only with resulting number"]},
        ]
        """
        return [{"role": message.role.name, "parts": [message.content]} for message in messages]
