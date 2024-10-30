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
from abc import abstractmethod
from dataclasses import dataclass
from typing import List
from cl.runtime import RecordMixin
from cl.convince.retrievers.retriever_key import RetrieverKey
from cl.runtime.primitive.timestamp import Timestamp


@dataclass(slots=True, kw_only=True)
class Retriever(RetrieverKey, RecordMixin[RetrieverKey], ABC):
    """Retrieves the requested data from the text."""

    def get_key(self) -> RetrieverKey:
        return RetrieverKey(retriever_id=self.retriever_id)

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""
        if self.retriever_id is None:
            self.retriever_id = Timestamp.create()

    # TODO: Use keyword params
    @abstractmethod
    def retrieve(
        self,
        input_text: str,
        param_description: str,
        param_samples: List[str] | None = None,
    ) -> str | None:
        """
        Retrieve the specified parameter from the entry (return None if the parameter is not found).

        Args:
            input_text: The text from which the data is extracted
            param_description: Parameter description
            param_samples: Optional parameter value samples for a few-shot prompt
        """
