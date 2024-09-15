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
from typing import Dict
from typing import Iterable
from typing import Type
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.generic_key import GenericKey
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.record_mixin import RecordMixin


@dataclass(slots=True, kw_only=True)
class GenericRecord:
    """Generic record can represent any record type."""

    key_type_str: str = missing()
    """Key type as dot-delimited string in module.ClassNameKey format inclusive of Key suffix if present."""

    key_fields: Iterable[str] = missing()
    """Names of primary key fields."""

    data_dict: Dict = missing()
    """Dictionary of data fields (including the primary key fields) in the order of declaration."""

    def get_key(self) -> KeyProtocol:
        key_dict = dict({k: v for k in self.key_fields if (v := self.data_dict.get(k, None)) is not None})
        raise NotImplementedError()
