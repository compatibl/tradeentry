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
from typing import List

import pytest

from cl.convince.llms.llm import Llm
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.convince.experiments.stub_llms import stub_full_llms
from stubs.cl.tradeentry.experiments.stub_json_utils import extract_json
from stubs.cl.tradeentry.experiments.stub_plot_utils import create_group_bar_plot

PROMPT_TEMPLATE = """Trade or leg description contains the following text. 

What is the payment frequency of this trade or leg?

Reply with JSON that has a single key 'pay_freq' whose value must be one of the following strings: 'ambiguous', '1m', '3m', '6m', '12m'.
No other values are allowed. Use 'ambiguous' when the text does not allow you to determine the frequency with certainty. "

Text: 
```
{text}
```"""


def _is_correct_answer(answer: dict, correct_answer: str) -> bool:
    return answer.get('pay_freq') == correct_answer


def _test_swap_freq(text: str, run_count: int, llm: Llm) -> List[str]:
    """Test swap frequency extraction from string."""

    prompt = PROMPT_TEMPLATE.format(text=text)

    results = []
    guard = RegressionGuard(channel=llm.llm_id)
    for trial_id in range(run_count):
        result = llm.completion(prompt, trial_id=trial_id)
        guard.write(result)
        results.append(result)
    return results

pytest.skip("Skip to allow GitHub actions to run without LLM keys.", allow_module_level=True)

def test_swap_freq():
    run_count = 50
    descriptions = [
        "Payment dates are January 15 and July 15",
        "Payments will be made on the 3rd of each month starting from January",
        "Payments are to be made on an annual basis"
    ]
    correct_answers = ["6m", "1m", "12m"]

    plot_values = []
    with TestingContext():
        for llm in stub_full_llms:
            for trade, correct_answer in zip(descriptions, correct_answers):
                results = _test_swap_freq(trade, run_count, llm)

                correct_answers_count = 0
                for result in results:
                    extracted_output = extract_json(result)
                    if extracted_output is None:
                        extracted_output = {}

                    correct_answers_count += int(_is_correct_answer(extracted_output, correct_answer))
                plot_values.append(round(correct_answers_count / run_count * 100, 2))

        plot_bar_labels = [llm.llm_id for llm in stub_full_llms]
        plot_group_labels = ["A", "B", "C"]
        fig = create_group_bar_plot(plot_values, plot_bar_labels, plot_group_labels)

    fig.savefig("test_swap_freq.png")
    RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
