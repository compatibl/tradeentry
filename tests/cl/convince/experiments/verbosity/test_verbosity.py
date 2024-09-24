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
from dateutil.relativedelta import relativedelta
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.plots.group_bar_plot import GroupBarPlot
from cl.runtime.testing.pytest.pytest_fixtures import local_dir_fixture
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


def test_verbosity(local_dir_fixture):
    """Test for verbosity."""

    with TestingContext():

        rep_count = 10
        prompt = (
            "Reply with the answer for 2 times 2. Your reply must include numerical value for the answer "
            "(not words) with no other comments or other text."
        )

        plot = GroupBarPlot()
        plot.values = []
        for llm in llms:
            completions = [llm.completion(prompt) for _ in range(rep_count)]
            mult = 100.0 / rep_count
            results = [
                ("Success", mult * sum(1 for x in completions if x == "4")),
                ("Allow EOL", mult * sum(1 for x in completions if x.replace("\n", "") == "4")),
                ("Allow whitespace", mult * sum(1 for x in completions if x.strip() == "4")),
                ("Allow comments", mult * sum(1 for x in completions if "4" in x)),
                ("Allow words", mult * sum(1 for x in completions if ("4" in x or "four" in x.lower()))),
            ]

            plot.values.extend([result[1] for result in results])

            # Apply group labels once
            if plot.group_labels is None:
                plot.group_labels = [result[0] for result in results]

        # Apply labels
        plot.bar_labels = [llm.llm_id for llm in llms]
        plot.group_labels = [result[1] for result in results]

        # Create and save
        fig = plot.create_figure()
        fig.savefig("test_verbosity.test_verbosity.png")

        # guard = RegressionGuard(channel=llm.llm_id)
        # guard.write(f"{result},{is_exact_match_yn},{is_trimmed_match_yn}")
        # guard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
