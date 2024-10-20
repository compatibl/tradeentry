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
from typing import Iterable
from cl.convince.prompts.extract.extract_prompt import ExtractPrompt
from cl.convince.prompts.prompt_keys import PromptKeys
from cl.runtime import Context
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.settings.preload_settings import PreloadSettings
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.convince.experiments.stub_llms import get_stub_full_llms


def _test_extract(entries: Iterable[str], params: Iterable[str]):
    """Test extraction of the specified parameters from the entries."""
    prompt = Context.current().load_one(ExtractPrompt, PromptKeys.BRACES_EXTRACT)
    if prompt is None:
        raise UserError(f"LLM record {prompt.prompt_id} is not found.")
    stub_full_llms = get_stub_full_llms()
    for llm in stub_full_llms:
        guard = RegressionGuard(channel=llm.llm_id)
        guard.write(f"entry,{','.join(params)}")
        for entry in entries:
            results = [entry] + [prompt.extract(llm, entry, param) for param in params]
            results_str = "\"" + "\",\"".join(results) + "\""
            guard.write(results_str)
    guard.verify_all()


def test_vanilla_swap_entry():
    """Test vanilla swap entry parameter extraction."""

    with TestingContext():
        # Preload data
        PreloadSettings.instance().preload()
        # Define parameters
        entries = [
            "Sell 10y SOFR swap at 3.45%",
        ]
        params = [
            "PayReceiveFixed",
            "Tenor",
            "RatesIndex",
            "FixedRate",
        ]
        # Run the test
        _test_extract(entries, params)


if __name__ == "__main__":
    pytest.main([__file__])
