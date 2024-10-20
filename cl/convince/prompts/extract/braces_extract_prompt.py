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

import re
from dataclasses import dataclass

from cl.convince.llms.llm import Llm
from cl.convince.llms.llm_key import LlmKey
from cl.convince.prompts.extract.extract_prompt import ExtractPrompt
from cl.runtime import Context
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.dataclasses_extensions import missing

_TRIPLE_BACKTICKS_RE = re.compile(r'```(.*?)```', re.DOTALL)
"""Regex for text between triple backticks."""

_BRACES_RE = re.compile(r'\{(.*?)\}')
"""Regex for text between curly braces."""


@dataclass(slots=True, kw_only=True)
class BracesExtractPrompt(ExtractPrompt):
    """Instructs the model to surround the requested parameter by curly braces."""

    preamble: str = missing()
    """Preamble is placed at the beginning of the prompt."""

    request: str = missing()
    """Request is placed at the end of the prompt."""

    def extract(self, llm_key: LlmKey, text: str, param: str) -> str:

        # Get LLM
        llm = Context.current().load_one(Llm, llm_key)
        if llm is None:
            raise UserError(f"LLM record {llm_key.llm_id} is not found.")

        # Strip whitespace from the original text
        text = text.strip()

        # Create braces extraction prompt
        formatted_request = self.request.format(text=text, param=param)
        formatted_prompt = f"""{self.preamble}{formatted_request}"""

        # Get text annotated with braces and check that the only difference is braces and whitespace
        annotated_text = llm.completion(formatted_prompt)
        between_backticks = self._extract_between_backticks(annotated_text)
        deannotated = between_backticks.replace("`", "").replace("{", "").replace("}", "").strip()
        if between_backticks != "NotFound" and deannotated != text:
            # Try one more time
            formatted_prompt = (f"{formatted_prompt}\n\nYou previously returned this text inside triple backticks: "
                                f"{between_backticks}\n"
                                f"However it does not meet the requirement that the only difference between "
                                f"the input and the output is curly braces. Please try again.")
            annotated_text = llm.completion(formatted_prompt).strip()
            between_backticks = self._extract_between_backticks(annotated_text)
            pass

        deannotated = between_backticks.replace("`", "").replace("{", "").replace("}", "").strip()
        if between_backticks != "NotFound" and deannotated != text:
            # TODO: Use unified diff
            raise UserError(f"Annotated text has changes other than curly braces.\n"
                            f"Original text: ```{text}```\n"
                            f"Annotated text: ```{between_backticks}```\n")

        # Extract data inside braces
        matches = re.findall(_BRACES_RE, between_backticks)
        for match in matches:
            if "{" in match or "}" in match:
                raise UserError(f"Nested curly braces are present in annotated text.\n"
                                f"Annotated text: ```{between_backticks}```\n")

        # Combine
        # TODO: Determine if numbered combination works better
        result = " ".join(matches)
        return result

    @classmethod
    def _extract_between_backticks(cls, text: str) -> str:
        # Find all occurrences of triple backticks and the text inside them
        matches = re.findall(_TRIPLE_BACKTICKS_RE, text)
        if len(matches) == 0:
            raise RuntimeError("No string found between triple backticks in: ", text)
        elif len(matches) > 1:
            raise RuntimeError("More than one string found between triple backticks in: ", text)
        result = matches[0].strip()
        return result
