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
from cl.runtime.context.context import Context
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.storage.data_source_types import TDataset
from cl.runtime.storage.data_source_types import TIdentity
from memoization import cached
from typing import Iterable, TypeVar, Generic
from typing import List
from typing import Type
from typing_extensions import Self

TKey = TypeVar("TKey", bound=KeyProtocol)


class RecordMixin(Generic[TKey]):
    """Optional mixin class for a record, code must not rely on inheritance from this class."""

    __slots__ = ()
    """To prevent creation of __dict__ in derived types."""

    @abstractmethod
    def get_key(self) -> KeyProtocol:
        """Return a new key object whose fields populated from self, do not implement to return self."""

    @classmethod
    @cached
    def get_query_types(cls) -> List[Type]:
        """
        Types that can be used to query for this type (in arbitrary order). Override if required.

        Notes:
            - The default implementation returns all classes in MRO where method `get_key` is not abstract.
            - The result is memoized (cached) for better performance.
        """

        # Get the list of classes in MRO that implement `get_key` method
        result = [
            c
            for c in cls.mro()
            if hasattr(c, "get_key")
            and callable(getattr(c, "get_key"))
            and not getattr(getattr(c, "get_key"), "__isabstractmethod__", False)
        ]

        # Make sure there is at least one such class in the returned list
        if len(result) == 0:
            # If the list is empty, the class itself does not implement `get_key` method
            raise RuntimeError(f"Class {cls.__module__}.{cls.__name__} does not implement `get_key` method.")

        return result

    @classmethod
    def load_many(
        cls,
        records_or_keys: Iterable[Self | TKey | None] | None,
        *,
        context: Context | None = None,
        dataset: TDataset = None,
        identities: Iterable[TIdentity] | None = None,
    ) -> Iterable[Self | None] | None:
        """
        Load records using an iterable of keys. A record passed instead of a key is returned without DB lookup.

        Args:
            records_or_keys: Iterable of records or keys (records are returned without DB lookup).
            context: Optional context, if None current context will be used
            dataset: Lookup dataset as a delimited string, list of levels, or None
            identities: Only the records whose identity matches one of the argument identities will be loaded
        """

        # Get data source from the current or specified context
        context = Context.current() if context is None else context
        data_source = context.data_source()
        result = data_source.load_many(records_or_keys, dataset=dataset, identities=identities)
        return result
