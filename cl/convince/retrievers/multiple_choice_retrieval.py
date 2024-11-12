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
from cl.runtime.records.dataclasses_extensions import missing
from cl.convince.retrievers.retrieval import Retrieval


@dataclass(slots=True, kw_only=True)
class MultipleChoiceRetrieval(Retrieval):
    """Retrieval type returned by AnnotatingRetriever."""

    input_text: str = missing()
    """Text from which the parameter is retrieved (input)."""

    param_description: str = missing()
    """Description of the retrieved parameter (input)."""

    valid_choices: List[str] = missing()
    """Valid choices for the retrieved parameter (input)."""

    success: str | None = None
    """Y when parameter was extracted and is one of the valid choices and N otherwise (output)."""

    param_value: str | None = None
    """Text with the retrieved parameter (output)."""

    justification: str | None = None
    """Justification (output)."""
