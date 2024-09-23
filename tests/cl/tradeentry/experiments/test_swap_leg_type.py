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
import uuid
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.testing.regression_guard import RegressionGuard
from cl.convince.llms.claude.claude_llm import ClaudeLlm
from cl.convince.llms.gemini.gemini_llm import GeminiLlm
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.llms.llama.fireworks.fireworks_llama_llm import FireworksLlamaLlm
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_floored_swap_entry, stub_basis_swap_entry, \
    stub_fixed_for_floating_swap_entry
from stubs.cl.tradeentry.experiments.stub_json_utils import extract_json

llms = [
    ClaudeLlm(llm_id="claude-3-sonnet-20240229"),
    FireworksLlamaLlm(llm_id="llama-v3-70b-instruct"),
    GeminiLlm(llm_id="gemini-1.5-flash"),
    GptLlm(llm_id="gpt-4o-mini"),
]

PROMPT_TEMPLATE = """You will be given the input below in the form of description of trade entry.

Return only JSON with following keys:
* Cap - bool, true if there is a cap in this trade
* Floor - bool, true if there is a floor in this trade
* FirstLegType - enum with values Floating and Fixed,
* SecondLegType - enum with values Floating and Fixed.

Description of trade entry:
```
{input_text}
```
Request id: {uuid}"""


def _test_swap_leg_type(trade_description: str):
    with TestingContext():
        uuid_num = uuid.uuid4()
        prompt = PROMPT_TEMPLATE.format(input_text=trade_description, uuid=uuid_num)
        run_count = 1
        for llm in llms:
            for _ in range(run_count):

                result = llm.completion(prompt)

                json_result = extract_json(result)
                if json_result is None:
                    json_result = "ERROR: can not extract json"

                guard = RegressionGuard(channel=llm.llm_id)
                guard.write(str(json_result))

        RegressionGuard.verify_all()


def test_basis_swap():
    _test_swap_leg_type(stub_basis_swap_entry)


def test_floored_swap():
    _test_swap_leg_type(stub_floored_swap_entry)


def test_fixed_for_floating_swap():
    _test_swap_leg_type(stub_fixed_for_floating_swap_entry)


if __name__ == "__main__":
    pytest.main([__file__])
