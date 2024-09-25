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
from stubs.cl.convince.experiments.stub_llms import stub_full_llms
from stubs.cl.tradeentry.experiments.stub_json_utils import extract_json
from stubs.cl.tradeentry.experiments.stub_plot_utils import create_group_bar_plot
from stubs.cl.tradeentry.experiments.stub_string_utils import sanitize_string
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_amortizing_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_basis_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_fixed_for_floating_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_floored_swap_entry


PROMPT_TEMPLATE = """You will be given the input below in the form of description of trade entry.

Return only JSON with following keys:
* Cap - bool, true if there is a cap in this trade
* Floor - bool, true if there is a floor in this trade
* FirstLegType - enum with values Floating and Fixed,
* SecondLegType - enum with values Floating and Fixed.

Description of trade entry:
```
{input_text}
```"""


def _is_correct_answer(answer: str, correct_answer: str) -> bool:
    sanitized_answer = sanitize_string(answer)
    sanitized_correct_answer = sanitize_string(correct_answer)

    return sanitized_answer == sanitized_correct_answer


def _testing_swap_leg_type(trade_description: str, run_count: int, llm: Llm) -> List[str]:

    prompt = PROMPT_TEMPLATE.format(input_text=trade_description)

    results = []
    guard = RegressionGuard(channel=llm.llm_id)
    for trial_id in range(run_count):
        result = llm.completion(prompt, trial_id=trial_id)
        guard.write(result)
        results.append(result)
    return results


def test_swap_leg_type():
    run_count = 2
    correct_answers = [
        "{'Cap': False, 'Floor': False, 'FirstLegType': 'Floating', 'SecondLegType': 'Fixed'}",
        "{'Cap': False, 'Floor': False, 'FirstLegType': 'Floating', 'SecondLegType': 'Floating'}",
        "{'Cap': False, 'Floor': True, 'FirstLegType': 'Floating', 'SecondLegType': 'Fixed'}",
        "{'Cap': False, 'Floor': False, 'FirstLegType': 'Floating', 'SecondLegType': 'Fixed'}",
    ]

    trades = [
        stub_fixed_for_floating_swap_entry,
        stub_basis_swap_entry,
        stub_floored_swap_entry,
        stub_amortizing_swap_entry,
    ]
    plot_values = []
    with TestingContext():
        for llm in stub_full_llms:
            for trade, correct_answer in zip(trades, correct_answers):
                results = _testing_swap_leg_type(trade, run_count, llm)

                correct_answers_count = 0
                for result in results:
                    extracted_output = extract_json(result)
                    correct_answers_count += int(_is_correct_answer(str(extracted_output), correct_answer))
                plot_values.append(round(correct_answers_count / run_count * 100, 2))

        plot_bar_labels = [llm.llm_id for llm in stub_full_llms]
        plot_group_labels = ["A", "B", "C", "D"]
        fig = create_group_bar_plot(plot_values, plot_bar_labels, plot_group_labels)

    fig.savefig("test_swap_leg_type.png")
    RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
