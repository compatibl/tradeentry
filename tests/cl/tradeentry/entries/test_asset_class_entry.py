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
from cl.convince.llms.claude.claude_llm import ClaudeLlm
from cl.convince.llms.llama.fireworks.fireworks_llama_llm import FireworksLlamaLlm
from cl.convince.llms.gemini.gemini_llm import GeminiLlm
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.tradeentry.entries.asset_class_entry import AssetClassEntry
from cl.tradeentry.trades.asset_class_keys import AssetClassKeys

llms = [
    ClaudeLlm(llm_id="claude-3-haiku-20240307"),
    FireworksLlamaLlm(llm_id="llama-v3-8b-instruct"),
    GeminiLlm(llm_id="gemini-1.5-flash"),
    GptLlm(llm_id="gpt-4o-mini"),
]


def test_smoke() -> None:
    """Smoke test."""
    with TestingContext():
        for llm in llms:
            entry = AssetClassEntry(
                entry_text="Swap",
                llm=llm
            )
            entry.process()
            assert entry.asset_class.asset_class_id == AssetClassKeys.rates.asset_class_id


if __name__ == "__main__":
    pytest.main([__file__])
