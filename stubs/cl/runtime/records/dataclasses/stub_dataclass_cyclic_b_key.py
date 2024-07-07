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

from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield
from cl.runtime.records.dataclasses.dataclass_key_mixin import DataclassKeyMixin
from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True)
class StubDataclassCyclicBKey(DataclassKeyMixin):
    """Stub class A with a field whose type is key for class B."""

    str_id: str = datafield()
    """String identifier for class A."""

    def get_generic_key(self) -> Tuple:
        return StubDataclassCyclicBKey, self.str_id
