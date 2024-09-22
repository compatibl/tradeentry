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
import datetime as dt
from typing import List
from dateutil.relativedelta import relativedelta
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.regression.regression_guard import RegressionGuard
from cl.convince.llms.claude.claude_llm import ClaudeLlm
from cl.convince.llms.llama.fireworks.fireworks_llama_llm import FireworksLlamaLlm
from cl.convince.llms.gemini.gemini_llm import GeminiLlm
from cl.convince.llms.gpt.gpt_llm import GptLlm

llms = [
    ClaudeLlm(llm_id="claude-3-haiku-20240307"),
    FireworksLlamaLlm(llm_id="llama-v3-8b-instruct"),
    GeminiLlm(llm_id="gemini-1.5-flash"),
    GptLlm(llm_id="gpt-4o-mini"),
]


def _test_extract_format(text: str, field_names: List[str]) -> None:
    """Test swap format extraction from string."""

    with TestingContext():

        prompt = f"""
Convert trade definition example provided in the following text to Python interpolated
string format by identifying specific values of fields from the provided list of fields
by their names in curly brackets.

Example:
* Sample text: ```1y AAPL call ATM```
* Sample fields: ```buy_or_sell, call_or_put, symbol, expiry```
* Sample output: ```{{expiry}} {{symbol}} call ATM```
Text: ```{text}``` Fields: ```{', '.join(field_names)} Your output: 
"""
        run_count = 1

        for llm in llms:
            for _ in range(run_count):

                result = llm.completion(prompt)

                guard = RegressionGuard(channel=llm.llm_id)
                guard.write(f"{result}")

        # TODO: guard.verify_all()


def test_swap_start_from_date_list():
    """Checks if the model can extract  format from an example."""
    _test_extract_format("10y SOFR swap at 3%", ["start", "maturity", "currency", "floating_index", "fixed_rate"])


if __name__ == "__main__":
    pytest.main([__file__])
