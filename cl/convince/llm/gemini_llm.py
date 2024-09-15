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
import google.generativeai as gemini
from cl.convince.llm.llm import Llm
from cl.convince.settings.gemini_settings import GeminiSettings

# Configure Gemini API key
gemini.configure(api_key=GeminiSettings.instance().api_key)


@dataclass(slots=True, kw_only=True)
class GeminiLlm(Llm):
    """Implements Gemini LLM API."""

    model_name: str | None = None
    """Model name in Gemini format including version if any, defaults to 'llm_id'."""

    def completion(self, query: str) -> str:

        model_name = self.model_name if self.model_name is not None else self.llm_id

        model = gemini.GenerativeModel(model_name=model_name)
        response = model.generate_content(query)

        result = response.text
        return result
