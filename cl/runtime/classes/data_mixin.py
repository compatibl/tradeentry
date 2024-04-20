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
from abc import ABC, abstractmethod
from typing import Any
from typing import Dict
from typing_extensions import Self

from cl.runtime.classes.class_info import ClassInfo


class DataMixin(ABC):
    """
    Optional mixin class for serializable data providing static type checkers with method signatures.

    Those methods that raise an exception must be overridden in derived types or by a decorator.
    They are not made abstract to avoid errors from static type checkers.

    The use of this class is optional. The code must not rely on inheritance from this class.
    """

    __slots__ = ()
    """To prevent creation of __dict__ in derived types."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        """Create from dictionary containing other dictionaries, lists and primitive types."""

        # Create record instance and populate it from dictionary
        serialized_class_path: str = data["_class"]
        serialized_class = ClassInfo.get_class_type(serialized_class_path)

        if not issubclass(serialized_class, cls):
            raise RuntimeError(f"Class {serialized_class.__name__} specified"
                               f"by the `_class` field in serialized data is not a subclass "
                               f"of {cls.__name__} into which this data is deserialized.")

        result = serialized_class()
        for key, value in data.items():
            if key != "_class" and key != "_match":
                setattr(result, key, value)
        return result
