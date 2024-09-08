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

from abc import abstractmethod
from cl.runtime.context.protocols import ContextProtocol
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.storage.data_source_types import TIdentity
from memoization import cached
from typing import Generic
from typing import Iterable
from typing import List
from typing import Type
from typing import TypeVar
from typing_extensions import Self

TKey = TypeVar("TKey", bound=KeyProtocol)


class RecordMixin(Generic[TKey]):
    """
    Optional mixin class for a record parameterized by its key, code must not rely on inheritance from this class.
    Using MyRecord(MyKey, RecordMixin[MyKey]) syntax provides additional methods to the record class.
    """

    __slots__ = ()
    """To prevent creation of __dict__ in derived types."""

    @abstractmethod
    def get_key(self) -> KeyProtocol:
        """Return a new key object whose fields populated from self, do not return self."""
