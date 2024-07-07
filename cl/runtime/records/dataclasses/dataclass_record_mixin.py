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

import dataclasses
from abc import ABC
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.storage.data_source_types import TField
from cl.runtime.storage.data_source_types import TPackedRecord
from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True, kw_only=True)
class DataclassRecordMixin(RecordMixin, ABC):
    """Mixin methods for dataclass records."""

    def to_dict(self) -> Dict[str, TField]:
        """Return TData for the contents."""
        return dataclasses.asdict(self)  # noqa

    def pack(self) -> TPackedRecord:
        # Get data dictionary and remove keys that have None values
        data_dict = dataclasses.asdict(self)
        data_dict = {k: v for k, v in data_dict.items() if v is not None}

        # Return a tuple of key and (record_type, serialized_data)
        return self.get_key(), (type(self), data_dict)
