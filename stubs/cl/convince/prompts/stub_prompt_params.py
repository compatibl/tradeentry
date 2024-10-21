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

from dataclasses import dataclass
from typing import List

from cl.runtime import RecordMixin
from cl.runtime.records.dataclasses_extensions import field
from stubs.cl.convince.prompts.stub_prompt_params_key import StubPromptParamsKey


@dataclass(slots=True, kw_only=True)
class StubPromptParams(StubPromptParamsKey, RecordMixin[StubPromptParamsKey]):
    """Stub prompt parameters of various primitive types."""

    str_req: str = "abc"
    """Required string field."""

    str_opt: str | None = None
    """Optional string field."""

    str_req_list: List[str] = field(default_factory=lambda: ["str_req_list_1", "str_req_list_2"])
    """Required string list field."""

    int_req: int = 123
    """Required int field."""

    int_opt: int | None = None
    """Optional int field."""

    float_req: float = 1.23
    """Required float field."""

    float_opt: int | None = None
    """Optional float field."""

    def get_key(self) -> StubPromptParamsKey:
        return StubPromptParamsKey(prompt_params_id=self.prompt_params_id)
