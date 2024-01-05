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
    Abstract base class for serializable data.

    Notes:
        The use of this class is optional. The code must not rely on inheritance from this class, but only on the
        presence of its methods. These methods may be implemented without using any specific base or mixin class.

        The methods that lack implementation must be overridden by a derived class in code or using a decorator.
        They are not made abstract to avoid errors from static type checkers in the latter case.
    """

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary containing other dictionaries, lists and primitive types."""
        raise RuntimeError(f"Method {type(self)}.to_dict() must be implemented in code or by a decorator.")

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Populate from a dictionary containing other dictionaries, lists and primitive types.
        Clears values for which the argument does not have a key.
        """
        raise RuntimeError(f"Method {type(self)}.from_dict() must be implemented in code or by a decorator.")
