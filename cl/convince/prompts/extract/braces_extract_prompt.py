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

from cl.convince.llms.llm import Llm
from cl.convince.llms.llm_key import LlmKey
from cl.convince.prompts.extract.extract_prompt import ExtractPrompt
from cl.runtime import Context
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.dataclasses_extensions import missing


@dataclass(slots=True, kw_only=True)
class BracesExtractPrompt(ExtractPrompt):
    """Instructs the model to surround the requested parameter by curly braces."""

    preamble: str = missing()
    """Preamble is placed at the beginning of the prompt."""

    request: str = missing()
    """Request is placed at the end of the prompt."""

    def extract(self, llm: LlmKey, text: str, param: str) -> str:
        llm_obj = Context.current().load_one(Llm, llm)
        if llm is None:
            raise UserError(f"LLM record {llm_obj.llm_id} is not found.")
        raise NotImplementedError()
