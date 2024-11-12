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
from cl.runtime.context.env_util import EnvUtil
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.experiments.experiment import Experiment
from cl.runtime.plots.group_bar_plot import GroupBarPlot
from cl.runtime.testing.regression_guard import RegressionGuard
from cl.convince.llms.llm import Llm
from cl.convince.retrievers.retriever_util import RetrieverUtil
from stubs.cl.convince.experiments.stub_llms import get_stub_mini_llms

_TEMPLATE = """You will be provided with an input text and a description of a parameter.
Your goal is to surround each piece of information about this parameter you find in the input text by curly braces.
Use multiple non-nested pairs of opening and closing curly braces if you find more than one piece of information.

You must reply with JSON formatted strictly according to the JSON specification in which all values are strings.
The JSON must have the following keys:

{{
    "success": <Y if at least one piece of information was found and N otherwise. This parameter is required.>
    "annotated_text": "<The input text where each piece of information about this parameter is surrounded by curly braces. There should be no changes other than adding curly braces, even to whitespace. Leave this field empty in case of failure.>,"
    "justification": "<Justification for your annotations in case of success or the reason why you were not able to find the parameter in case of failure.>"
}}

Input text: ```{InputText}```
Parameter description: ```The words Buy or Sell, or the words Pay Fixed or Receive Fixed```
{Examples}
"""


def _test_brace_annotation_few_shot(
    trade_description: str,
    run_count: int,
    llm: Llm,
    examples: str = "",
) -> List[str]:

    prompt = _TEMPLATE.format(InputText=trade_description, Examples=examples)

    results = []
    for trial_id in range(run_count):
        result = llm.completion(prompt, trial_id=trial_id)

        guard = RegressionGuard(channel=llm.llm_id)
        guard.write(result)

        results.append(result)

    return results


def test_brace_annotation_few_shot():
    with TestingContext():
        run_count = 10
        correct_answer = "{Sell} 10y SOFR swap at 3.45%"
        trade = "Sell 10y SOFR swap at 3.45%"
        labels = ["Zero-Shot", "Few-Shot", "Adverse Few-Shot"]
        plot_bar_labels = []
        plot_group_labels = []
        plot_values = []

        examples = {
            "Zero-Shot": "",
            "Few-Shot": """
Examples:
Input: Buy 5y LIBOR swap at 2.25%
Annotated: {Buy} 5y LIBOR swap at 2.25%""",
            "Adverse Few-Shot": """
Here are examples of correct annotations and common mistakes:

Correct annotation:
Input: Buy 5y LIBOR swap at 2.25%
Annotated: "{Buy} 5y LIBOR swap at 2.25%"

Common mistake 1 - Annotating irrelevant information:
Input: Bank sells 5y LIBOR swap at 3.55%
Incorrect: {Bank sells} 5y LIBOR swap at 3.55%
Correct: Bank {sells} 5y LIBOR swap at 3.55%

Common mistake 2 - Add field name after the value:
Input: Buy 7y LIBOR swap at 3.75%
Incorrect: Buy {Buy or Sell} 7y LIBOR swap at 3.75%
Correct: {Buy} 7y LIBOR swap at 3.75%""",
        }

        # Create Llm objects for test
        stub_mini_llms = get_stub_mini_llms()

        for llm in stub_mini_llms:
            for label in labels:
                results = _test_brace_annotation_few_shot(trade, run_count, llm, examples[label])

                correct_answers_count = 0
                for result in results:
                    json_result = RetrieverUtil.extract_json(result)
                    if json_result is None:
                        continue
                    annotated_text = json_result.get("annotated_text", None)

                    correct_answers_count += int(annotated_text == correct_answer)

                plot_bar_labels.append(llm.llm_id)
                plot_group_labels.append(label)
                plot_values.append(round(correct_answers_count / run_count * 100, 2))

        plot = GroupBarPlot(
            plot_id="accuracy",
            bar_labels=plot_bar_labels,
            group_labels=plot_group_labels,
            values=plot_values,
            value_ticks=list(range(0, 101, 10)),
        )
        plot.save_png()

    # Regression test
    RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
