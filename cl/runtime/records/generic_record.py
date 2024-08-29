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

from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.generic_key import GenericKey
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.storage.data_source_types import TDataDict
from dataclasses import dataclass
from typing import Iterable
from typing import Type


@dataclass(slots=True, kw_only=True)
class GenericRecord(RecordMixin[KeyProtocol]):
    """Generic record can represent any record type."""

    key_type: Type = missing()
    """Key type."""

    key_fields: Iterable[str] = missing()
    """Names of primary key fields."""

    data_dict: TDataDict = missing()
    """Dictionary of data fields (including the primary key fields) in the order of declaration."""

    def get_key(self) -> KeyProtocol:
        key_dict = dict({k: v for k in self.key_fields if (v := self.data_dict.get(k, None)) is not None})
        return GenericKey(key_type=self.key_type, key_dict=key_dict)
