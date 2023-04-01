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
from typing import Any, Dict


class Data(ABC):
    """
    Base class for serializable data.

    Instances of direct descendants of the Data class can be stored in a
    database as fields of a Record class, but not on their own. Derive
    from Record to enable storing instances directly.

    Derived classes must implement the following methods:

    * to_dict() - serialize self as dictionary
    * from_dict(data_dict) - populate self from dictionary
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize self as dictionary (may return shallow copy).

        The result may be returned using shallow copy. The callers of this method
        must serialize or perform deep copy of the result in case the record fields
        change after this method is invoked.
        """

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Populate self from dictionary (must perform deep copy).

        The implementation of this method perform deep copy of the input
        in case the argument dictionary changes after this method is invoked.
        """

