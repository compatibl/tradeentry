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
from typing import List

from cl.convince.retrievers.multiple_choice_retrieval import MultipleChoiceRetrieval
from cl.runtime import Context
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.convince.entries.entry import Entry
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.llms.llm import Llm
from cl.convince.llms.llm_key import LlmKey
from cl.convince.prompts.formatted_prompt import FormattedPrompt
from cl.convince.prompts.prompt import Prompt
from cl.convince.prompts.prompt_key import PromptKey
from cl.convince.retrievers.retrieval import Retrieval
from cl.convince.retrievers.retriever import Retriever
from cl.convince.retrievers.retriever_util import RetrieverUtil

_TRIPLE_BACKTICKS_RE = re.compile(r"```(.*?)```", re.DOTALL)
"""Regex for text between triple backticks."""

_BRACES_RE = re.compile(r"\{(.*?)\}")
"""Regex for text between curly braces."""

_TEMPLATE = """You will be provided with an input text, a description of a parameter, and possible values of this parameter.
Your goal is to extract the value of the parameter from the provided input text.

You must reply with JSON formatted strictly according to the JSON specification in which all values are strings.
The JSON must have the following keys:

{{
    "success": "<Y if you successfully extracted the parameter value and it matches one of the provided choices and N otherwise. This field is required.>",
    "param_value": "<Parameter value you extracted which matches one of the provided choices. Leave this field empty in case of failure.>",
    "justification": "<Justification for the parameter value you extracted in case of success or the reason why you were not able to find the parameter in case of failure. This field is required.>"
}}
Input text: ```{InputText}```
Parameter description: ```{ParamDescription}```
Semicolon-delimited list of valid choices: ```{ValidChoices}```

Keep in mind that the input text does not need to be one of the valid choices. Rather, you must use your knowledge as
Senior Quantitative Analyst to determine if the input has the same meaning or maps to one of the valid choices,
without necessarily being exactly the same or having the same format.

Examples:
  - When input text is $, a valid choice may be USD
  - When input text is %, a valid choice may be percent
"""


@dataclass(slots=True, kw_only=True)
class MultipleChoiceRetriever(Retriever):
    """Instructs the model to select the value of parameter from the provided choices."""

    llm: LlmKey = missing()
    """LLM used to perform the retrieval."""

    prompt: PromptKey = missing()
    """Prompt used to perform the retrieval."""

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""
        if self.llm is None:
            self.llm = GptLlm(llm_id="gpt-4o")  # TODO: Review the handling of defaults
        if self.prompt is None:
            self.prompt = FormattedPrompt(
                prompt_id="MultipleChoiceRetriever",
                params_type=MultipleChoiceRetrieval.__name__,  # TODO: More detailed error message for mismatch
                template=_TEMPLATE,
            )  # TODO: Review the handling of defaults

    def retrieve(
        self,
        *,
        input_text: str,
        param_description: str,
        valid_choices: List[str],
    ) -> MultipleChoiceRetrieval:
        # Get LLM and prompt
        context = Context.current()
        llm = Context.current().load_one(Llm, self.llm)
        prompt = Context.current().load_one(Prompt, self.prompt)
        valid_choices_str = "; ".join(valid_choices)

        trial_count = 2
        for trial_index in range(trial_count):

            # Generate trial label
            trial_label = str(trial_index)
            is_last_trial = trial_index == trial_count - 1

            # Strip starting and ending whitespace
            input_text = input_text.strip()  # TODO: Perform more advanced normalization

            # Create a retrieval record
            retrieval = MultipleChoiceRetrieval(
                retriever=self.get_key(),
                trial_label=trial_label,
                input_text=input_text,
                param_description=param_description,
                valid_choices=valid_choices,
            )

            try:
                # Create braces extraction prompt
                rendered_prompt = prompt.render(params=retrieval)

                # Get text annotated with braces and check that the only difference is braces and whitespace
                completion = llm.completion(rendered_prompt, trial_id=trial_label)

                # Extract the results
                json_result = RetrieverUtil.extract_json(completion)
                if json_result is not None:
                    retrieval.success = json_result.get("success", None)
                    retrieval.param_value = json_result.get("param_value", None)
                    retrieval.justification = json_result.get("justification", None)
                    context.save_one(retrieval)
                else:
                    retrieval.success = "N"
                    retrieval.justification = (f"Could not extract JSON from the LLM response. "
                                               f"LLM response:\n{completion}\n")
                    context.save_one(retrieval)
                    raise UserError(retrieval.justification)

                # Normalize output
                if retrieval.success is not None:
                    retrieval.success = retrieval.success.strip()
                if retrieval.param_value is not None:
                    retrieval.param_value = retrieval.param_value.strip()

                # Self-reported success or failure
                success = Entry.parse_required_bool(retrieval.success, field_name="success")
                if not success:
                    # Parameter is not found, continue with the next trial
                    continue

                if StringUtil.is_not_empty(retrieval.param_value):
                    # Check that extracted_value is one of the provided choices
                    if retrieval.param_value not in valid_choices:
                        if not is_last_trial:
                            # Continue if not the last trial
                            continue
                        else:
                            # Otherwise report an error
                            # TODO: Use unified diff
                            raise UserError(
                                f"The extracted parameter is among the valid choices.\n"
                                f"Extracted value: ```{retrieval.param_value}```\n"
                                f"Semicolon-delimited list of valid choices: ```{valid_choices_str}```\n"
                            )
                else:
                    raise RuntimeError(
                        f"Extraction success reported by {llm.llm_id}, however "
                        f"the annotated text is empty. Input text:\n{input_text}\n"
                    )

                # Return retrieval
                return retrieval

            except Exception as e:
                retrieval.success = "N"
                retrieval.justification = str(e)
                context.save_one(retrieval)
                if is_last_trial:
                    # Rethrow only when the last trial is reached
                    raise UserError(
                        f"Unable to extract parameter from the input text after {trial_count} trials.\n"
                        f"Input text: {input_text}\n"
                        f"Parameter description: {param_description}\n"
                        f"Last trial error information: {retrieval.justification}\n"
                    )
                else:
                    # Otherwise continue
                    pass

        # The method should always return from the loop, adding as a backup in case this changes in the future
        raise UserError(
            f"Unable to extract parameter from the input text.\n"
            f"Input text: {input_text}\n"
            f"Parameter description: {param_description}\n"
        )
