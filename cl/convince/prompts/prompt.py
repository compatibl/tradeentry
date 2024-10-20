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

from abc import ABC
from dataclasses import dataclass
from cl.runtime import RecordMixin
from cl.runtime.records.dataclasses_extensions import missing
from cl.convince.prompts.prompt_key import PromptKey


@dataclass(slots=True, kw_only=True)
class Prompt(PromptKey, RecordMixin[PromptKey], ABC):
    """The prompt begins from the preamble and ends with the request, with supporting information in the middle."""

    def get_key(self) -> PromptKey:
        return PromptKey(prompt_id=self.prompt_id)
