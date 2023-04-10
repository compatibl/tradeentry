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
from dataclasses import asdict, dataclass
from typing import Any, Dict

from cl.runtime.core.storage.data import Data


@dataclass
class ClassData(Data, ABC):
    """
    Base class for polymorphic types where all serializable
    data is stored in dataclass fields.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize self as dictionary.

        Default implementation uses runtime class introspection.
        Derived classes may override for greater performance.
        """
        return asdict(self)

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Populate self from dictionary.

        Default implementation uses runtime class introspection.
        Derived classes may override for greater performance.
        """
        raise NotImplementedError()  # TODO: currently a stub
        pass
