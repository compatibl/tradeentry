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
from cl.convince.llm.anthropic_llm import AnthropicLlm


def test_smoke():
    """Test AnthropicLlm class."""

    llms = [
        AnthropicLlm(llm_id="claude-3-haiku-20240307"),
    ]

    with TestingContext():
        for llm in llms:
            assert "4" in llm.completion("2 times 2?")


if __name__ == "__main__":
    pytest.main([__file__])
