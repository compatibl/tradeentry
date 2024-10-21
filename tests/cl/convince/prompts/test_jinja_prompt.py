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
from cl.convince.prompts.jinja_prompt import JinjaPrompt
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.convince.prompts.stub_prompt_params import StubPromptParams

_TEMPLATE = "StrReq='{{StrReq}}' StrOpt='{{StrOpt}}' IntReq='{{IntReq}}' IntOpt='{{IntOpt}}'"


def test_jinja_prompt():
    """Smoke test."""

    with TestingContext():
        prompt = JinjaPrompt(prompt_id="Default", template=_TEMPLATE, params_type=StubPromptParams.__name__)
        guard = RegressionGuard()
        guard.write(prompt.render(StubPromptParams(str_opt="def", int_opt=456)))
        try:
            prompt.render(StubPromptParams())
        except UserError as e:
            guard.write(f"Expected UserError: {e}")
        RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
