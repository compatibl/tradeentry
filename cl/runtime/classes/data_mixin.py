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
from typing import Any
from typing import Dict
from typing_extensions import Self


class DataMixin(ABC):
    """
    Optional mixin class for serializable data providing static type checkers with method signatures.

    Those methods that raise an exception must be overridden in derived types or by a decorator.
    They are not made abstract to avoid errors from static type checkers.

    The use of this class is optional. The code must not rely on inheritance from this class.
    """

    __slots__ = []  # Adding an empty __slots__ declaration prevents the creation of a __dict__ for every instance

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary containing other dictionaries, lists and primitive types."""
        raise RuntimeError(
            f"Method to_dict() for class {type(self).__name__} in module {type(self).__module__} "
            f"is neither implemented in code nor by a decorator."
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        """Create from dictionary containing other dictionaries, lists and primitive types."""
        result = cls()
        for key, value in data.items():
            if key != "_type" and key != "_chain":
                setattr(result, key, value)
        return result
