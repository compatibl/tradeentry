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

from abc import abstractmethod, ABC
from dataclasses import dataclass
from cl.convince.prompts.prompt import Prompt
from cl.runtime import RecordMixin
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.convince.prompts.prompt_key import PromptKey
from cl.runtime.records.protocols import TDataDict
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer

_data_serializer = DictSerializer()
"""Serializer used to serialize params object for rendering the template."""

_key_serializer = StringSerializer()
"""Serializer used to serialize keys for error reporting."""


@dataclass(slots=True, kw_only=True)
class TemplatePrompt(Prompt, ABC):
    """Uses a template to render the prompt, param names are PascalCase in curly braces."""

    template: str = missing()
    """Uses a template to render the prompt, param names are PascalCase in curly braces."""

    def get_key(self) -> PromptKey:
        return PromptKey(prompt_id=self.prompt_id)

    def render(self, params: RecordMixin) -> str:
        """Use data from the parameters object of 'params_type' to render the template."""
        # Check params type
        self._check_params_type(params)
        # Serialize and convert keys to PascalCase
        params_dict = _data_serializer.serialize_data(params)
        params_dict_with_pascal_case_keys = {CaseUtil.snake_to_pascal_case(k): v for k, v in params_dict.items() if v is not None}
        # Render
        try:
            result = self._render(params_dict_with_pascal_case_keys)
        except KeyError as e:
            field_name = str(e)
            params_key_str = _key_serializer.serialize_key(params.get_key())
            present_keys_str = "".join(f"  - {x}\n" for x in params_dict_with_pascal_case_keys.keys())
            raise UserError(f"Parameter required by prompt is either None or not a field of the parameters object.\n"
                            f"Prompt key='{self.prompt_id}'\n"
                            f"Parameter name: {field_name}\n"
                            f"Parameters object type={type(params).__name__} and key='{params_key_str}'\n"
                            f"Available non-empty fields of the parameters object:\n{present_keys_str}\n")
        return result

    @abstractmethod
    def _render(self, dict_with_pascal_case_keys: TDataDict) -> str:
        """Protected method performing the actual rendering, must throw KeyError if a parameter is missing."""
