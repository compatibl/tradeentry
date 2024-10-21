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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from cl.runtime import RecordMixin
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.dataclasses_extensions import missing
from cl.convince.prompts.prompt_key import PromptKey
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.schema.schema import Schema


@dataclass(slots=True, kw_only=True)
class Prompt(PromptKey, RecordMixin[PromptKey], ABC):
    """Parameterized LLM prompt template rendered using a parameters object."""

    params_type: str = missing()
    """Record whose pascalized fields are used as template parameters in ClassName format."""

    def get_key(self) -> PromptKey:
        return PromptKey(prompt_id=self.prompt_id)

    @abstractmethod
    def render(self, params: RecordMixin) -> str:
        """Use data from the parameters object of 'params_type' to render the template."""

    def _check_params_type(self, params: Any) -> None:
        """Check that params object is an instance of the right type."""
        params_type = Schema.get_type_by_short_name(self.params_type)
        if not isinstance(params, params_type):
            actual_type_str = type(params).__name__
            raise UserError(f"Parameters object for prompt {self.prompt_id} has type {actual_type_str} which "
                            f"is not a subclass of the expected type {self.params_type}.")
