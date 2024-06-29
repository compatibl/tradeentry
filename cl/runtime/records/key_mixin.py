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
from typing import Tuple


class KeyMixin(ABC):
    """Optional mixin class for a primary key object."""

    __slots__ = ()
    """To prevent creation of __dict__ in derived types."""

    @abstractmethod
    def get_generic_key(self) -> Tuple:
        """Return a tuple of key type and key fields."""

    def __hash__(self):
        """Calculate hash based on key type and values, must not change key fields after hashing."""
        return hash(self.get_generic_key())


class KeysMixin(ABC):
    """Optional mixin class for an iterable of primary key objects."""

    __slots__ = ()
    """To prevent creation of __dict__ in derived types."""

    @abstractmethod
    def get_generic_keys(self) -> Tuple:
        """Return a tuple of key type and lists of key fields."""
