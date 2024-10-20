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

import pytest
from typing import List
from cl.convince.prompts.extract.braces_extract_prompt import BracesExtractPrompt
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.convince.experiments.stub_llms import get_stub_full_llms

PROMPT_PREAMBLE = """You will be provided with an input text and a description of a parameter.
Your goal is to surround each piece of information about this parameter you find in the input text by curly braces.
Use multiple non-nested pairs of opening and closing curly braces if you find more than one piece of information.

You must reply with JSON formatted strictly according to the JSON specification in which all values are strings.
The JSON must have the following keys:

{{
    "success": <Y if at least one piece of information was found and N otherwise. This parameter is required.>
    "annotated_text": "<The input text where each piece of information about this parameter is surrounded by curly braces. There should be no changes other than adding curly braces, even to whitespace. Leave this field empty in case of failure.>,"
    "justification": "<Justification for your annotations in case of success or the reason why you were not able to find the parameter in case of failure.>"
}}
"""

PROMPT_REQUEST = """
Input text: ```{input_text}```
Parameter description: ```{param_description}``
"""

ENTRY_TEXT = "Sell 10y SOFR swap at 3.45%"
PARAM_DESCRIPTION = "Fixed rate."
PARAM_SAMPLES = [
    "Pay fixed",
    "We pay fixed",
    "Long",
    "Buy",
    "Receive fixed",
    "Rec fixed",
    "We receive fixed",
    "Short",
    "Sell",
]


def _test_extract(entry_text: str, param_description: str, param_samples: List[str] | None = None) -> None:
    """Test extraction of the specified parameters from the entries."""
    param_samples_str = "".join(f"  - {x}\n" for x in param_samples) if param_samples is not None else None
    prompt = BracesExtractPrompt(
        prompt_id="test_braces_extract_prompt",
        preamble=PROMPT_PREAMBLE,
        request=PROMPT_REQUEST
    )
    stub_full_llms = get_stub_full_llms()
    for llm in stub_full_llms:
        guard = RegressionGuard(channel=llm.llm_id)
        annotated_text = prompt.extract(llm, entry_text, param_description)
        guard.write(f"Input Text: {entry_text} Extracted Value: {annotated_text}")
    RegressionGuard.verify_all()


def test_no_samples():
    """Smoke test."""

    with TestingContext():
        _test_extract(ENTRY_TEXT, PARAM_DESCRIPTION)


if __name__ == "__main__":
    pytest.main([__file__])
