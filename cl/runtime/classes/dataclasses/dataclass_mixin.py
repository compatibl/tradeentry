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

from __future__ import annotations
from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any, Tuple, Type, Dict
from typing_extensions import Self

from cl.runtime.classes.record_mixin import RecordMixin


@dataclass(slots=True)
class DataclassMixin(RecordMixin, ABC):
    """Mixin methods for dataclass records."""

    def to_dict(self) -> Tuple[Tuple[Type, ...], Type[Self], Dict[str, Any]]:
        return self.get_key(), self.__class__, asdict(self)

