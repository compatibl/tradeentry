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
from typing import Dict

from cl.runtime.records.data_mixin import DataMixin
from cl.runtime.storage.data_source_types import TField
from dataclasses import dataclass


# TODO: Consolidate in the same module with other dataclass mixins
@dataclass(slots=True, kw_only=True)
class DataclassDataMixin(DataMixin):
    """Mixin methods for dataclass records."""

    def to_dict(self) -> Dict[str, TField]:
        """Return TData for the contents."""
        return dataclasses.asdict(self)  # noqa
