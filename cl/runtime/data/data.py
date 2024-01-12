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
from typing_extensions import Self
from typing import Any, Dict


class Data(ABC):
    """
    Optional mixin class for serializable data.

    The use of this class is optional. The code must not rely on inheritance from this class, but only on the
    presence of its methods. These methods may be implemented without using any specific base or mixin class.

    The methods that lack implementation must be overridden by a derived class in code or using a decorator.
    They are not made abstract to avoid errors from static type checkers in the latter case.
    """

    __slots__ = []
    """Adding empty __slots__ prevents creation of __dict__ for every instance."""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary containing other dictionaries, lists and primitive types."""
        raise RuntimeError(f"Method to_dict() for class {type(self).__name__} in module {type(self).__module__} "
                           f"is neither implemented in code nor by a decorator.")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        """Create from dictionary containing other dictionaries, lists and primitive types."""
        result = cls()
        for key, value in data.items():
            if key != "_t":
                setattr(result, key, value)
        return result
