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
from cl.convince.retrievers.retrieval_key import RetrievalKey


@dataclass(slots=True, kw_only=True)
class Retrieval(RetrievalKey, RecordMixin[RetrievalKey]):
    """Retrieves the requested data from the text."""

    input_text: str
    """Text from which the parameter is retrieved."""

    param_description: str
    """Description of the retrieved parameter."""

    param_samples: List[str] | None = None
    """Samples of possible retrieved parameter values for few-shot prompts."""

    success: bool | None = None
    """True for success and False for failure (populated after the retrieval and may be used by a validating prompt)."""

    param_value: str | None = None
    """Value of the extracted parameter (populated after the retrieval and may be used by a validating prompt)."""

    justification: str | None = None
    """Justification (populated after the retrieval and may be used by a validating prompt)."""

    def get_key(self) -> RetrievalKey:
        return RetrievalKey(retrieval_id=self.retrieval_id)
