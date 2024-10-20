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

from cl.convince.entries.entry import Entry
from cl.convince.llms.llm import Llm
from cl.convince.llms.llm_key import LlmKey
from cl.convince.prompts.extract.extract_prompt import ExtractPrompt
from cl.runtime import Context
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.records.dataclasses_extensions import missing
from stubs.cl.tradeentry.experiments.stub_json_utils import extract_json

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

    def extract(self, llm_key: LlmKey, input_text: str, param_description: str) -> str:  # TODO: Add TrialID prefix here

        # Get LLM
        llm = Context.current().load_one(Llm, llm_key)
        if llm is None:
            raise UserError(f"LLM record {llm_key.llm_id} is not found.")

        # Strip whitespace from the original text
        input_text = input_text.strip()

        # Create braces extraction prompt
        formatted_request = self.request.format(input_text=input_text, param_description=param_description)
        formatted_prompt = f"""{self.preamble}{formatted_request}"""

        trial_count = 2
        for trial_index in range(trial_count):
            is_last_trial = (trial_index == trial_count - 1)
            try:
                # Get text annotated with braces and check that the only difference is braces and whitespace
                completion = llm.completion(formatted_prompt, trial_id=trial_index)

                # Extract the results
                json_result = extract_json(completion)  # TODO(Major): Do not depend on stubs
                if json_result is None:
                    raise UserError(f"NCould not extract JSON from the LLM response. LLM response:\n{completion}\n")
                success_text = json_result.get("success", None)
                annotated_text = json_result.get("annotated_text", None)
                justification = json_result.get("justification", None)

                # Go to the next trial in case of failure
                success = Entry.parse_required_bool(success_text, field_name="success_text")
                if not success:
                    continue

                if StringUtil.is_not_empty(annotated_text):
                    # Compare after removing the curly brackets
                    to_compare = self._deannotate(annotated_text)
                    if to_compare != input_text:
                        if not is_last_trial:
                            # Continue if not the last trial
                            continue
                        else:
                            # Otherwise report an error
                            # TODO: Use unified diff
                            raise UserError(f"Annotated text has changes other than curly braces.\n"
                                            f"Input text: ```{input_text}```\n"
                                            f"Annotated text: ```{annotated_text}```\n")
                else:
                    raise RuntimeError(f"Extraction success reported by {llm.llm_id}, however "
                                       f"the annotated text is empty. Input text:\n{input_text}\n")

                # Extract data inside braces
                matches = re.findall(_BRACES_RE, annotated_text)
                for match in matches:
                    if "{" in match or "}" in match:
                        if not is_last_trial:
                            continue
                        else:
                            raise UserError(f"Nested curly braces are present in annotated text.\n"
                                            f"Annotated text: ```{annotated_text}```\n")

                # Combine and return from inside the loop
                # TODO: Determine if numbered combination works better
                result = " ".join(matches)
                return result

            except Exception as e:
                if is_last_trial:
                    # Rethrow only when the last trial is reached
                    raise UserError(f"Unable to extract parameter from the input text after {trial_count} trials.\n"
                                    f"Input text: {input_text}\n"
                                    f"Parameter description: {param_description}\n"
                                    f"Last trial error information: {str(e)}\n")
                else:
                    # Otherwise log the error details and continue
                    pass  # TODO: Log failure with info message level

        # The method should always return from the loop, adding as a backup in case this changes in the future
        raise UserError(f"Unable to extract parameter from the input text.\n"
                        f"Input text: {input_text}\n"
                        f"Parameter description: {param_description}\n")

    @classmethod
    def _extract_annotated(cls, text: str) -> str:
        # Find all occurrences of triple backticks and the text inside them
        matches = re.findall(_TRIPLE_BACKTICKS_RE, text)
        if len(matches) == 0:
            raise RuntimeError("No string found between triple backticks in: ", text)
        elif len(matches) > 1:
            raise RuntimeError("More than one string found between triple backticks in: ", text)
        result = matches[0].strip()
        return result

    @classmethod
    def _extract_in_braces(cls, annotated_text: str, *, continue_on_error: bool | None = None) -> str | None:  # TODO: Move to Util class
        """
        Extract the blocks inside curly braces.

        Notes:
            - Return as semicolon-delimited string if more than one block is found
            - If continue_on_error is True, return None without raising an error
        """
        matches = re.findall(_BRACES_RE, annotated_text)
        if len(matches) == 0:
            if continue_on_error:
                return None
            else:
                raise UserError(f"No curly braces are present in annotated text.\n"
                                f"Annotated text: ```{annotated_text}```\n")
        if any("{" in match or "}" in match for match in matches):
            if continue_on_error:
                return None
            else:
                raise UserError(f"Nested curly braces are present in annotated text.\n"
                                f"Annotated text: ```{annotated_text}```\n")

        # Combine using semicolon delimiter and return
        result = ";".join(matches)
        return result

    @classmethod
    def _deannotate(cls, text: str) -> str:
        # Remove triple backticks and curly brackets
        result = text.replace("`", "").strip().replace("{", "").replace("}", "").strip()
        return result

