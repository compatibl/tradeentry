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
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.testing.regression_guard import RegressionGuard
from cl.convince.llms.claude.claude_llm import ClaudeLlm
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.llms.llama.fireworks.fireworks_llama_llm import FireworksLlamaLlm

llms = [
    ClaudeLlm(llm_id="claude-3-5-sonnet-20240620"),
    FireworksLlamaLlm(llm_id="llama-v3-70b-instruct"),
    GptLlm(llm_id="gpt-4o-2024-08-06"),
]


def _test_swap_freq(text: str):
    """Test swap frequency extraction from string."""

    with TestingContext():

        prompt = (
            f"Trade or leg description contains the following text. "
            f"What is the payment frequency of this trade or leg? "
            f"Reply with JSON that has a single key 'pay_freq' whose "
            f"value must be one of the following strings: "
            f"'???', '1m', '3m', '6m', '12m'. "
            f"No other values are allowed. Use 'ambiguous' when the"
            f"text does not allow you to determine the frequency with certainty. "
            f"Text: {text}"
        )
        run_count = 1

        for llm in llms:
            for _ in range(run_count):

                result = llm.completion(prompt)

                answers = {"???", "1m", "3m", "6m", "12m"}
                is_allowed_value_yn = "Y" if result in answers else "N"
                is_trimmed_allowed_value_yn = "Y" if result.strip() in answers else "N"

                guard = RegressionGuard(channel=llm.llm_id)
                guard.write(f"{result},{is_allowed_value_yn},{is_trimmed_allowed_value_yn}")

        guard.verify_all()


def test_swap_freq_from_date_list():
    """From a list of dates, frequency is implicit."""
    _test_swap_freq("Payment dates are January 15 and July 15")


if __name__ == "__main__":
    pytest.main([__file__])
