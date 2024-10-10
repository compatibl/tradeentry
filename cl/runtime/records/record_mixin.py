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
from typing import Callable
from typing import Generic
from typing import Type
from typing import TypeVar
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.records.record_util import RecordUtil

TKey = TypeVar("TKey", bound=KeyProtocol)  # TODO: Remove duplicate TKey definition


class RecordMixin(Generic[TKey]):
    """
    Optional mixin class for a record, code must not rely on inheritance from this class.
    Derive MyRecord from both MyKey and RecordMixin[MyKey] as in MyRecord(MyKey, RecordMixin[MyKey]).
    """

    __slots__ = ()
    """To prevent creation of __dict__ in derived types."""

    @abstractmethod
    def get_key(self) -> TKey:
        """Return a new key object whose fields populated from self, do not return self."""

    def init_all(self) -> None:
        """Invoke 'init' for each class in the order from base to derived, then validate against schema."""
        RecordUtil.init_all(self)


