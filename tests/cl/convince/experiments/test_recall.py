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
from cl.convince.llm.anthropic_llm import AnthropicLlm
from cl.convince.llm.fireworks_llm import FireworksLlm
from cl.convince.llm.gemini_llm import GeminiLlm
from cl.convince.llm.openai_llm import OpenaiLlm
from cl.runtime.regression.regression_guard import RegressionGuard

llms = [
    AnthropicLlm(llm_id="claude-3-haiku-20240307"),
    FireworksLlm(llm_id="llama-v3-8b-instruct"),
    GeminiLlm(llm_id="gemini-1.5-flash"),
    OpenaiLlm(llm_id="gpt-4o-mini"),
]


def _test_recall(text: str):
    """Test the specified recall string."""

    with TestingContext():

        prompt = (f"Reply with the following text changing nothing in it at all. "
                  f"I will check that the text matches exactly. This is a test. Text: {text}")
        run_count = 1

        for llm in llms:
            for _ in range(run_count):

                result = llm.completion(prompt)

                is_exact_match_yn = "Y" if result == text else "N"
                is_trimmed_match_yn = "Y" if result.strip() == text.strip() else "N"

                guard = RegressionGuard(channel=llm.llm_id)
                guard.write(f"{result},{is_exact_match_yn},{is_trimmed_match_yn}")

        # TODO: guard.verify_all()


def test_known_phrase():
    """Test the specified recall string."""
    _test_recall("A quick brown fox jumps over the lazy dog")


def test_modified_known_phrase():
    """Test the specified recall string."""
    _test_recall("A quick brownie dog jumps over the lazy dog")


def test_random_chars():
    """Test the specified recall string."""
    _test_recall("AasaREl 3022a1 CEoaS aSpWAmaQ &8(1 pSozar")


def test_long_table():
    """Test the specified recall string."""
    origin_date = dt.date(2003, 4, 21)
    row_count = 10
    row_list = [
        f"{origin_date + relativedelta(months=3*i)},{1_000_000 * (i if i > 10 else 10)}"
        for i in range(row_count)
    ]
    table = "\n".join(row_list)
    _test_recall(table)


if __name__ == "__main__":
    pytest.main([__file__])
