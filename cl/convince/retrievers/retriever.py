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
from typing import Any, List

from cl.convince.entries.entry import Entry
from cl.runtime import RecordMixin
from cl.runtime.log.exceptions.user_error import UserError
from cl.convince.retrievers.retriever_key import RetrieverKey
from cl.runtime.schema.schema import Schema


@dataclass(slots=True, kw_only=True)
class Retriever(RetrieverKey, RecordMixin[RetrieverKey], ABC):
    """Retrieves the requested data from the text."""

    def get_key(self) -> RetrieverKey:
        return RetrieverKey(retriever_id=self.retriever_id)

    @abstractmethod
    def retrieve(self,
                 entry: Entry,
                 param_description: str,
                 param_samples: List[str] | None = None
                 ) -> Entry:
        """
        Retrieve the specified parameter from the entry and return it as a smaller entry.

        Args:
            entry: The entry from which the data is extracted
            param_description: Parameter description
            param_samples: Optional parameter value samples for a few-shot prompt
        """
