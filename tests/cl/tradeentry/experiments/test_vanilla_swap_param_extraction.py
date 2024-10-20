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
from typing import Dict, List, Tuple
from matplotlib import pyplot as plt

from cl.convince.prompts.extract.braces_extract_prompt import BracesExtractPrompt
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.plots.group_bar_plot import GroupBarPlot
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.convince.experiments.stub_llms import get_stub_full_llms
from stubs.cl.tradeentry.experiments.stub_json_utils import extract_json
from stubs.cl.tradeentry.experiments.stub_tag_utils import add_line_numbers
from stubs.cl.tradeentry.experiments.stub_tag_utils import fields_to_text
from stubs.cl.tradeentry.experiments.stub_trade_checker import StubFormattedStringChecker
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_amortizing_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_floored_swap_entry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_vanilla_swap_entry

PROMPT_TEMPLATE = """Follow these instructions precisely and adhere to the requested format.

You will be provided with a trade entry text and a description of a trade parameter below.
You must reply with JSON that is properly formatted according to the JSON specification and has the following keys:

{{
    "annotated_text": "<The input trade entry text in triple backticks where each piece of information about this parameter is surrounded by curly braces. There should be no changes to the input text other than adding curly braces.>,"
    "justification": "<An optional justification for your annotated text or for the reason why you were not able to find the parameter.>"
}}

Trade entry text: ```{entry}```
Description of a trade parameter: ```{description}``

Here are some of the samples for how the information about this parameter may look like:

{samples}
"""

TRADE_ENTRY = "Sell 10y SOFR swap at 3.45%"

PARAMS = [
    (
        "PayReceiveFixed",
        "User input to determine if we pay or receive fixed leg coupons in a fixed-for-floating swap.",
        [
            "Pay fixed",
            "We pay fixed",
            "Long",
            "Buy",
            "Receive fixed",
            "Rec fixed",
            "We receive fixed",
            "Short",
            "Sell",
        ],
        "Sell",
    )
]


def _test_extraction(entry: str, params: List[Tuple[str, str, List[str], str]]) -> None:
    # Create Llm objects for test
    stub_full_llms = get_stub_full_llms()

    trial_count = 1
    plot_bar_labels = []
    plot_group_labels = []
    plot_values = []
    for llm in stub_full_llms:
        for param_name, param_description, param_samples, param_value in params:
            param_samples_str = "".join(f"  - {x}\n" for x in param_samples)
            prompt = PROMPT_TEMPLATE.format(entry=entry, description=param_description, samples=param_samples_str)
            success_count = 0
            for trial_id in range(trial_count):
                # Invoke LLM
                completion = llm.completion(prompt, trial_id=trial_id)
                # Process result
                json_result = extract_json(completion)
                guard = RegressionGuard(channel=llm.llm_id)
                if json_result is not None:
                    annotated_text = json_result.get("annotated_text", "None")
                    justification = json_result.get("justification", "None")
                    extracted_text = BracesExtractPrompt._extract_in_braces(annotated_text, continue_on_error=True)
                    success = extracted_text.strip() == param_value.strip()  # TODO: Use specialized class for comparisons
                    success_count = success_count + 1 if success else success_count
                    success_str = "Y" if success else "N"
                    guard.write(f"Success: {success_str} Extracted: {extracted_text} "
                                f"Annotated: {annotated_text} Justification: {justification}")
                else:
                    guard.write("Error: Could not extract JSON.")
            success_fraction = min(max(round(success_count / trial_count * 100, 2), 0), 100)

            plot_bar_labels.append(llm.llm_id)
            plot_group_labels.append(param_name)
            plot_values.append(success_fraction)

    plot = GroupBarPlot(
        plot_id="Accuracy",
        bar_labels=plot_bar_labels,
        group_labels=plot_group_labels,
        values=plot_values,
        value_ticks=list(range(0, 101, 10)),
    )
    plot.save_png()
    RegressionGuard.verify_all()


def test_vanilla_swap():
    with TestingContext():
        _test_extraction(TRADE_ENTRY, PARAMS)


if __name__ == "__main__":
    pytest.main([__file__])
