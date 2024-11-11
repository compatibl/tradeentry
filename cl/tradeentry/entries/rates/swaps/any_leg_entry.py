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

from cl.convince.entries.entry import Entry
from cl.convince.entries.entry_key import EntryKey
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.retrievers.retriever_util import RetrieverUtil
from cl.runtime import Context
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.dataclasses_extensions import missing
from cl.tradeentry.entries.rates.swaps.fixed_swap_leg_entry import FixedSwapLegEntry
from cl.tradeentry.entries.rates.swaps.float_swap_leg_entry import FloatSwapLegEntry

_PROMPT_TEMPLATE = """You will be given the input below in the form of description of trade entry leg.

Return only JSON with following keys:
* LegType - enum with values Floating and Fixed

Description of trade entry leg:
```
{input_text}
```"""


@dataclass(slots=True, kw_only=True)
class AnyLegEntry(Entry):
    """Capture any leg type from user input, leg type is determined from the input."""

    leg: EntryKey = missing()
    """Entry for the leg."""

    def determine_leg_type(self, leg_type_prompt: str) -> str | None:
        llm = GptLlm(llm_id="gpt-4o")
        input_text = self.description

        trial_count = 2
        for trial_index in range(trial_count):

            # Generate trial label
            trial_label = str(trial_index)
            is_last_trial = trial_index == trial_count - 1

            try:
                # Create a brace extraction prompt using input parameters
                rendered_prompt = leg_type_prompt.format(input_text=input_text)

                # Run completion
                completion = llm.completion(rendered_prompt, trial_id=trial_label)

                # Extract the results
                json_result = RetrieverUtil.extract_json(completion)
                if json_result is not None:
                    leg_type = json_result.get("LegType", None)
                    if leg_type != 'Fixed' and leg_type != 'Floating':
                        raise UserError(f"Undefined leg type: {leg_type}")

                else:
                    raise UserError(f"Could not extract JSON from the LLM response. "
                                    f"LLM response:\n{completion}\n")

                return leg_type

            except Exception as e:
                if is_last_trial:
                    # Rethrow only when the last trial is reached
                    raise UserError(
                        f"Unable to extract parameter from the input text after {trial_count} trials.\n"
                        f"Input text: {input_text}\n"
                        f"Last trial error information: {str(e)}\n"
                    )
                else:
                    # Otherwise continue
                    pass

        # The method should always return from the loop, adding as a backup in case this changes in the future
        raise UserError(
            f"Unable to extract parameter from the input text.\n"
            f"Input text: {input_text}\n"
        )

    def run_generate(self) -> None:
        """Determine the leg type from the input and create an object of the corresponding type."""

        leg_type = self.determine_leg_type(_PROMPT_TEMPLATE)

        if leg_type == 'Floating':
            leg_obj = FloatSwapLegEntry(description=self.description)
        elif leg_type == 'Fixed':
            leg_obj = FixedSwapLegEntry(description=self.description)
        else:
            raise UserError(f"Undefined leg type: {leg_type}")

        leg_obj.run_generate()
        self.leg = leg_obj.get_key()

        Context.current().save_one(leg_obj)
        Context.current().save_one(self)
