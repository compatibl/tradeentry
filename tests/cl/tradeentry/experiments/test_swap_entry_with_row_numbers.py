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
import json
import re
from typing import Dict
from typing import List
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.regression.regression_guard import RegressionGuard
from cl.convince.llms.claude.claude_llm import ClaudeLlm
from cl.convince.llms.gemini.gemini_llm import GeminiLlm
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.llms.llama.fireworks.fireworks_llama_llm import FireworksLlamaLlm
from stubs.cl.tradeentry.experiments.stub_tag_utils import add_line_numbers
from stubs.cl.tradeentry.experiments.stub_tag_utils import fields_to_text
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_amortizing_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_basis_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_floored_swap_entry

llms = [
    ClaudeLlm(llm_id="claude-3-sonnet-20240229"),
    FireworksLlamaLlm(llm_id="llama-v3-70b-instruct"),
    GeminiLlm(llm_id="gemini-1.5-flash"),
    GptLlm(llm_id="gpt-4o-mini"),
]

PROMPT_TEMPLATE = """You will be given a description of a trade entry with numbered rows, followed by a list of fields to identify within that text.
Your task is to find relevant information about the field and reference the row where you find the information.

Here is the input trade entry:
```
{input_text}
```

The description of the fields you need to identify:
```
{fields}
```

Each field description contain datatype and occurrences type.
If the occurrences type is single you should look for a single place among that contains the most relevant information about the field.
If the occurrences type is multiple you should include every place that has information relevant to the field.
Datatype helps you understand what data you are looking for. However, when you are asked to get the piece of data you should copy it and return as a string always.

For each field you should do the following:
1. Find all data corresponding to the field in the trade entry.
2. If the occurrence type is single, then select only one piece of data that is the most relevant, if the occurrence type is multiple, then select all of them.
3. For every such piece of data create the following dictionary
{{
    "data": <piece of data, string>,
    "row": <the row number in the trade entry, integer>
}}
4. If the occurrence type is single, then the output should be one dictionary, if the occurrence type is multiple, then the answer should be list of dictionaries.
5. If there is no piece of data that has relevant information than the generated dictionary should have empty string snd zero integer as default values.

Generate json dictionary with the field names as keys. The above algorith, describes how to create value for every field.

Enclose json in triple single quotes and ensure that it is parsable."""

FIELDS = [
    {"name": "FloatLegCurrency", "type": "string", "freq": "single"},
    {"name": "FloatLegIndex", "type": "string", "freq": "single"},
    {"name": "FloatLegSpread", "type": "float", "freq": "single"},
    {"name": "FloatLegFrequency", "type": "string", "freq": "single"},
    {"name": "FloatLegDaycountBasis", "type": "string", "freq": "single"},
    {"name": "FixedLegCurrency", "type": "string", "freq": "single"},
    {"name": "FixedLegFixedRate", "type": "float", "freq": "single"},
    {"name": "FixedLegFrequency", "type": "string", "freq": "single"},
    {"name": "FixedLegDaycountBasis", "type": "string", "freq": "single"},
    {"name": "StartDate", "type": "date", "freq": "single"},
    {"name": "NotionalResetDate", "type": "date", "freq": "multiple"},
    {"name": "NotionalAmount", "type": "float", "freq": "multiple"},
]


def _test_answer_referencing(fields: List[Dict], trade_description: str):
    fields_text = fields_to_text(fields)

    with TestingContext():

        prompt = PROMPT_TEMPLATE.format(input_text=trade_description, fields=fields_text)
        run_count = 1
        for llm in llms:
            for _ in range(run_count):
                result = llm.completion(prompt)
                guard = RegressionGuard(channel=llm.llm_id)
                guard.write(result)

    # TODO: guard.verify_all()


def test_basis_swap():
    numbered_basis_swap = add_line_numbers(stub_basis_swap_entry)
    _test_answer_referencing(FIELDS, numbered_basis_swap)


def test_floored_swap():
    numbered_floored_swap = add_line_numbers(stub_floored_swap_entry)
    _test_answer_referencing(FIELDS, numbered_floored_swap)


def test_notional_schedule_swap():
    numbered_notional_schedule_swap = add_line_numbers(stub_amortizing_swap_entry)
    _test_answer_referencing(FIELDS, numbered_notional_schedule_swap)


if __name__ == "__main__":
    pytest.main([__file__])
