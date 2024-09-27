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

from cl.convince.llms.claude.claude_llm import ClaudeLlm
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.convince.llms.llama.fireworks.fireworks_llama_llm import FireworksLlamaLlm

stub_mini_llms = [
    FireworksLlamaLlm(llm_id="llama-v3-8b-instruct"),
    GptLlm(llm_id="gpt-4o-mini"),
]
"""Mini-LLMs for proof of concept tests."""

stub_full_llms = [
    ClaudeLlm(llm_id="claude-3-5-sonnet-20240620"),
    FireworksLlamaLlm(llm_id="llama-v3-70b-instruct"),
    GptLlm(llm_id="gpt-4o"),
]
"""Full (but not extravagant) LLMs for prompt design tests."""
