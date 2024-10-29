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

import pandas as pd
import pytest
from typing import List

from cl.convince.entries.entry import Entry
from cl.convince.retrievers.retriever_util import RetrieverUtil
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.plots.group_bar_plot import GroupBarPlot
from cl.runtime.testing.regression_guard import RegressionGuard
from cl.convince.llms.llm import Llm
from stubs.cl.convince.experiments.stub_llms import get_stub_mini_llms, get_stub_full_llms

_TEMPLATE = """You are tasked with evaluating the similarity between two trades in the context of a specific parameter. Your goal is to provide a similarity score from 1 to 100, where 1 means completely different and 100 means identical. Pay close attention to the format and wording of the trades, but do not focus on numerical differences.

Here is the description of the basic trade:
```
{BasicTrade}
```

Here is the description of the trade to be evaluated:
```
{EvaluatedTrade}
```

The parameter for comparison is described as follows:
```
{ParameterDescription}
```

Analyze the two trade descriptions, focusing on their similarities and differences in the context of the given parameter. Consider the structure, wording, and overall format of the trades, but do not place emphasis on specific numerical values that may differ.

Provide a detailed justification for your similarity assessment, explaining the key factors that influenced your decision. Consider both the similarities and the differences you observed.

After your justification, assign a similarity score from 1 to 100, where:
0 = The trades are completely different in terms of the given parameter
100 = The trades are identical in terms of the given parameter

Present your response in JSON with the following format:
{{
    "analysis": <Your detailed justification for the similarity assessment, single line>,
    "similarity_score": <Your numerical score between 0 and 100>
}}
"""


def _test_vanilla_swap_similarity(basic_trade: str, evaluated_trade: str, parameter_description: str, run_count: int, llm: Llm,) -> List[str]:

    prompt = _TEMPLATE.format(BasicTrade=basic_trade, EvaluatedTrade=evaluated_trade,
                              ParameterDescription=parameter_description)

    results = []
    for trial_id in range(run_count):

        result = llm.completion(prompt, trial_id=trial_id)

        guard = RegressionGuard(channel=llm.llm_id)
        guard.write(f"{basic_trade}\n{evaluated_trade}\n{result}")

        results.append(result)

    return results


def test_vanilla_swap_similarity():
    with TestingContext():
        run_count = 1
        basic_trade = "Sell 10y SOFR swap at 3.45%"
        parameter_description = "The words Buy or Sell, or the words Pay Fixed or Receive Fixed"
        evaluated_trades = ["Sell 10y SOFR swap at 3.55%", "Sell 10y LIBOR swap at 3.45%",
                            "Sell 10y LIBOR swap at 3.55%", "Sell 5y LIBOR swap at 3.55%",
                            "Bank sells 5y LIBOR swap at 3.55%", "Bank sells 10y SOFR swap at 3.45%",
                            "Short 10y SOFR fixed at 3.45%", "10y SOFR payer at 3.45%",
                            "Short 10y LIBOR fixed at 3.45%", "7y SOFR payer at 2.55%",
                            "Buy 10y SOFR swap at 3.45%", "Buy 5y LIBOR swap at 3.55%"]
        summary_results = []
        stub_full_llms = get_stub_full_llms()
        for evaluated_trade in evaluated_trades:
            summary_result_row = {'Basic Trade': basic_trade, 'Evaluated Trade': evaluated_trade}
            for llm in stub_full_llms:
                results = _test_vanilla_swap_similarity(basic_trade, evaluated_trade, parameter_description, run_count, llm)
                for result in results:
                    json_result = RetrieverUtil.extract_json(result)
                    if json_result is None:
                        continue
                    similarity_score = json_result.get("similarity_score", None)
                    summary_result_row[llm.llm_id] = similarity_score
            summary_results.append(summary_result_row)

        results_df = pd.DataFrame(summary_results)
        summary_guard = RegressionGuard(channel="summary")
        summary_guard.write(results_df.to_string(index=False))

    RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
