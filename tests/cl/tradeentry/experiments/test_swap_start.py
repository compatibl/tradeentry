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
from cl.convince.llms.gemini.gemini_llm import GeminiLlm
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.llms.llama.fireworks.fireworks_llama_llm import FireworksLlamaLlm

llms = [
    ClaudeLlm(llm_id="claude-3-haiku-20240307"),
    FireworksLlamaLlm(llm_id="llama-v3-8b-instruct"),
    GeminiLlm(llm_id="gemini-1.5-flash"),
    GptLlm(llm_id="gpt-4o-mini"),
]


def _test_swap_start(text: str):
    """Test swap start date extraction from string."""

    with TestingContext():

        prompt = (
            f"We need to determine the accrual start date (the start date when the interest begins accruing, "
            f"which may not be the same as payment date) of this trade or leg. "
            f"Given the following text, reply with JSON that has the following keys only where "
            f"value is true if we need to know this field in addition to the text to answer this question, "
            f"and false if we do not need it. "
            f"Keys: 'payment_frequency', 'floating_frequency', 'pays_in_arrears', 'currency', 'maturity_date'. "
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

        # TODO: guard.verify_all()


def test_swap_start_from_date_list():
    """Checks if the model has internal knowledge of the rules for setting payment date."""
    _test_swap_start("The first payment is on July 15")


if __name__ == "__main__":
    pytest.main([__file__])
