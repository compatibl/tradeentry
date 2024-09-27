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
from cl.runtime.testing.regression_guard import RegressionGuard
from cl.convince.llms.llm import Llm
from stubs.cl.convince.experiments.stub_llms import get_stub_full_llms
from stubs.cl.tradeentry.experiments.stub_plot_utils import create_group_bar_plot
from stubs.cl.tradeentry.experiments.stub_string_utils import extract_between_backticks
from stubs.cl.tradeentry.experiments.stub_string_utils import sanitize_string
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_amortizing_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_basis_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_fixed_for_floating_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_floored_swap_entry

PROMPT_TEMPLATE = """In this text, surround information about each leg in curly brackets. Make no other changes
to the text. Take into account the following:

- Only one set of curly brackets per leg should be present, surrounding the information specific to the leg
- Include information about who pays the leg
- Do not surround with curly brackets any text that is not specific to a single leg
- Do not miss any information from the original text

Text: 
```
{text}
```

Enclose you output text in triple backticks."""


def _is_correct_answer(answer: str, trade_description: str, correct_answers: List[str]) -> bool:
    sanitized_answer = sanitize_string(answer)
    sanitized_trade_description = sanitize_string(trade_description)

    return sanitized_answer.replace("{", "").replace("}", "") == sanitized_trade_description and all(
        correct_answer in answer for correct_answer in correct_answers
    )


def _test_surrounding_leg(trade_description: str, run_count: int, llm: Llm) -> List[str]:

    prompt = PROMPT_TEMPLATE.format(text=trade_description)

    results = []
    for trial_id in range(run_count):

        result = llm.completion(prompt, trial_id=trial_id)

        guard = RegressionGuard(channel=llm.llm_id)
        guard.write(result)

        results.append(result)

    return results


def test_surrounding_leg():
    run_count = 50
    correct_answers = [
        [
            "{Bank pays: 6M USD Term SOFR, semi-annual, act/360}",
            "{Bank receives: USD fixed 3.45%, semi-annual, act/360}",
        ],
        [
            "{Client pays 3M Term SOFR + 70bps (act/360, quarterly)}",
            "{Client receives 12M Term SOFR (act/360, annual)}",
        ],
        [
            "{We pay: 6M USD Term SOFR (floating), semi-annual, act/360}",
            "{We receive: USD fixed 3.45%, semi-annual, act/360}",
        ],
        [
            "{Party A pays: 6M USD Term SOFR (floating), semi-annual, act/360}",
            "{Party A receives: USD fixed 3.20%, semi-annual, act/360}",
        ],
    ]
    trades = [
        stub_fixed_for_floating_swap_entry,
        stub_basis_swap_entry,
        stub_floored_swap_entry,
        stub_amortizing_swap_entry,
    ]
    plot_values = []
    with TestingContext():
        # Create Llm objects for test
        stub_full_llms = get_stub_full_llms()

        for llm in stub_full_llms:
            for trade, correct_answer in zip(trades, correct_answers):
                results = _test_surrounding_leg(trade, run_count, llm)

                correct_answers_count = 0
                for result in results:
                    extracted_output = extract_between_backticks(result)
                    correct_answers_count += int(_is_correct_answer(extracted_output, trade, correct_answer))

                plot_values.append(round(correct_answers_count / run_count * 100, 2))

        plot_bar_labels = [llm.llm_id for llm in stub_full_llms]
        plot_group_labels = ["C", "B", "D", "E"]
        fig = create_group_bar_plot(plot_values, plot_bar_labels, plot_group_labels)
    fig.savefig("test_surrounding_leg_with_curly_brackets.png")

    # Regression test
    RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
