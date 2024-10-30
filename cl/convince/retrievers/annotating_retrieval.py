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
from cl.convince.retrievers.multiple_choice_retrieval import Retrieval
from cl.runtime.records.dataclasses_extensions import missing


@dataclass(slots=True, kw_only=True)
class AnnotatingRetrieval(Retrieval):
    """Retrieval type returned by AnnotatingRetriever."""

    input_text: str = missing()
    """Text from which the parameter is retrieved (input)."""

    param_description: str = missing()
    """Description of the retrieved parameter (input)."""

    is_required: bool = missing()
    """If False, not found is considered a success (input)."""

    param_samples: List[str] | None = None
    """Samples of possible retrieved parameter values for few-shot prompts (input)."""

    success: str | None = None
    """Y for success and N for failure (output)."""

    annotated_text: str | None = None
    """Annotated text (output)."""

    justification: str | None = None
    """Justification (output)."""

    output_text: str | None = None
    """Output text inside one or several curly brace blocks (output)."""
