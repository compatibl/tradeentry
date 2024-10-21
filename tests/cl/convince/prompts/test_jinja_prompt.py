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

_SIMPLE_TEMPLATE = "StrReq='{{StrReq}}' StrOpt='{{StrOpt}}' IntReq='{{IntReq}}' IntOpt='{{IntOpt}}'"
_FOR_LOOP_TEMPLATE = "{% for item in StrReqList %}- {{item}}{% endfor %}"


def test_jinja_prompt():
    """Smoke test."""

    with TestingContext():
        guard = RegressionGuard()
        params_type = StubPromptParams.__name__
        simple_prompt = JinjaPrompt(prompt_id="Default", template=_SIMPLE_TEMPLATE, params_type=params_type)
        for_loop_prompt = JinjaPrompt(prompt_id="Default", template=_FOR_LOOP_TEMPLATE, params_type=params_type)

        # Simple prompt
        guard.write(simple_prompt.render(StubPromptParams(str_opt="def", int_opt=456)))
        # Jinja2 renders missing params as empty string, no error is thrown
        guard.write(simple_prompt.render(StubPromptParams()))
        # For loop
        guard.write(for_loop_prompt.render(StubPromptParams()))
        RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
