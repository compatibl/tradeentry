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
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.regression.regression_guard import RegressionGuard
from cl.convince.llms.claude.claude_llm import ClaudeLlm
from cl.convince.llms.llama.fireworks.fireworks_llama_llm import FireworksLlamaLlm
from cl.convince.llms.gemini.gemini_llm import GeminiLlm
from cl.convince.llms.gpt.gpt_llm import GptLlm

llms = [
    ClaudeLlm(llm_id="claude-3-opus-20240229"),
    FireworksLlamaLlm(llm_id="llama-v3-70b-instruct"),
    # TODO: API error, investigate GeminiLlm(llm_id="gemini-1.5-pro"),
    GptLlm(llm_id="gpt-4o"),
]

PROMPT_TEMPLATE = """
You are tasked with converting a trade definition example to a Python interpolated string format. 
Your goal is to identify specific values in the input text that correspond to the provided field names
and replace them with the appropriate field names in curly brackets.

Here is the input text:
```
{text}
```

The available fields are:
```
{fields}
```

To complete this task, follow these steps:
1. Analyze the input text and identify which words or phrases correspond to the available fields.
2. Replace each identified word or phrase with the corresponding available field name in curly brackets,
   similar to the formatted Python string.
3. If two of such words of phrases follow each other without space, do not combine available field names
   under a single set of curly brackets.
4. Keep any words or phrases that don't match a field name as they are.

Here's an example of how this process works for a different trade type:
Input text: "1y AAPL call ATM"
Available fields: "buy_or_sell, call_or_put, symbol, expiry"
Output: "{{expiry}} {{symbol}} {{call_or_put}} ATM"

Now, convert the given input text using the provided fields by following these guidelines:

1. If a field is not present in the input text, do not include it in the output.
2. If there are words or phrases in the input text that don't correspond to any field, 
   treat them as ordinary text even if they seem like parameters.
3. If an available field is not present but a related field is, do not use your knowledge of finance 
   to derive one from the other (for example, do not derive currency from index).
4. However if an available field is not present but another field is that has unambiguous,
   one-to-one correspondence with the available field it can be returned instead (for example, 
   effective date instead of start date).

Make sure your answer contains only the converted text, with no additional explanation or commentary.

Your work will be tested by substituting field values back into the formatted string you will output
and checking that the resulting string is exactly the same as the output you received.
"""

vanilla_swap_entry = """
Sell 10y SOFR swap at 3.45%
"""

fixed_for_floating_swap_entry = """
Swap Details:
Notional: 10,000,000,000
Bank pays: 6M USD Term SOFR, semi-annual, act/360
Bank receives: USD fixed 3.45%, semi-annual, act/360
Notional exchange: None
Start date: 21-Apr-2023
Tenor: 10 years
"""


def _test_extract_format(text: str, field_names: List[str]) -> None:
    """Test swap format extraction from string."""

    with (TestingContext()):

        prompt = PROMPT_TEMPLATE.format(text=text, fields=', '.join(field_names))

        run_count = 1

        for llm in llms:
            for _ in range(run_count):
                result = llm.completion(prompt)

                guard = RegressionGuard(channel=llm.llm_id)
                guard.write(f"{result}")

        # TODO: guard.verify_all()


def test_vanilla():
    """Checks if the model can extract format from an example with brief trade description."""
    _test_extract_format(
        vanilla_swap_entry,
        [
            "pay_or_receive_fixed",
            "start_date",
            "maturity_date",
            "swap_length"
            "fixed_rate",
            "floating_index",
            "fixed_leg_payment_currency",
            "floating_leg_payment_currency",
            "fixed_leg_daycount_basis",
            "floating_leg_daycount_basis"
            "fixed_leg_payment_frequency",
            "floating_leg_payment_frequency",
        ])


def test_fixed_for_floating():
    """Checks if the model can extract format from an example with more verbose trade description."""
    _test_extract_format(
        fixed_for_floating_swap_entry,
        [
            "pay_or_receive_fixed",
            "start_date",
            "maturity_date",
            "swap_length"
            "fixed_rate",
            "floating_index",
            "fixed_leg_payment_currency",
            "floating_leg_payment_currency",
            "fixed_leg_daycount_basis",
            "floating_leg_daycount_basis"
            "fixed_leg_payment_frequency",
            "floating_leg_payment_frequency",
        ])


if __name__ == "__main__":
    pytest.main([__file__])
