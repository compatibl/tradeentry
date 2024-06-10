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
from abc import abstractmethod
from cl.runtime.context.context import Context
from cl.runtime.records.record_util import RecordUtil
from cl.runtime.storage.data_source_types import TDataset
from cl.runtime.storage.data_source_types import TKey
from cl.runtime.storage.data_source_types import TLoadedRecord
from cl.runtime.storage.data_source_types import TPackedRecord
from memoization import cached
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Type
from typing_extensions import Self

_NONE = 0  # Code indicating None
_KEY = 1  # Code indicating tuple
_RECORD = 2  # Code indicating record
_UNKNOWN = 3  # Code indicating unknown type


class RecordMixin(ABC):
    """
    Optional mixin class for database records providing static type checkers with method signatures.

    Those methods that raise an exception must be overridden in derived types or by a decorator.
    They are not made abstract to avoid errors from static type checkers.

    The use of this class is optional. The code must not rely on inheritance from this class.

    Records may implement handlers and/or viewers:

    - Handlers are methods that can be invoked from the UI
    - Viewers are methods whose return value is displayed in the UI
    - Both may be instance, class or static methods, and may have parameters
    """

    __slots__ = ()
    """To prevent creation of __dict__ in derived types."""

    @abstractmethod
    def get_key(self) -> Tuple:
        """Return (type(self), primary key fields), identifying all field types in returned value type hint."""

    @abstractmethod
    def pack(self) -> TPackedRecord:
        """Return (TKey, TData) where TKey is (type, primary key fields) and TData is serialized record data."""

    def init(self) -> None:
        """Similar to __init__ but uses previously set fields instead of parameters (not invoked by data source)."""

        # Do nothing by default
        pass

    def validate(self) -> None:
        """Validate previously set fields (invoked by data source before saving and after loading)."""

        # Do nothing by default
        pass

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
        cls: Self,
        records_or_keys: List[Self | TKey | None],
        *,
        context: Context | None = None,
        dataset: TDataset = None,
    ) -> List[Self | None]:
        """
        Load serialized records from a single table using a list of keys.
        If records are passed instead of keys, they are returned without data source lookup.

        Returns:
            Iterable of records with the same length and in the same order as the list of keys.
            The result element is None if the record is not found or the key is None.

        Args:
            records_or_keys: Each element is TLoadedRecord, TKey, or None
            context: Optional context, if None current context will be used
            dataset: Lookup dataset as a delimited string, list of levels, or None
        """
        return RecordUtil.load_many(cls, records_or_keys, context=context, dataset=dataset)
