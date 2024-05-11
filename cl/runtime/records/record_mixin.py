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
from cl.runtime.storage.data_source_types import GenericKey
from cl.runtime.storage.data_source_types import GenericRecord, GenericPack
from cl.runtime.rest.context import Context
from memoization import cached
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
        """
        Return tuple of (type, primary key fields).

        Notes:
            Implementation for MyType must narrow the returned type hint to Tuple[MyType, ...].
        """

    @abstractmethod
    def pack(self) -> GenericPack:
        """Return tuple of (KEY, DATA) where KEY=(type, primary key fields) and DATA is serialized record data."""

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
    def get_base_type(cls) -> Type:
        """
        Base type determines the table where this type is stored. Override if required.

        Notes:
            - The default implementation returns the last class in MRO where method `get_key` is not abstract.
            - The result is memoized (cached) for better performance.
        """

        # The implementation must not use `get_query_types` method because it may be overridden

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

        # Return the last class in the list
        return result[-1]

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
        records_or_keys: List[GenericRecord | GenericKey | None],
        dataset: List[str] | str | None = None,
        *,
        context: Context | None = None,
    ) -> List[Self | None]:
        """
        Load serialized records from a single table using a list of keys in tuple format.
        If records are passed instead of keys, they are returned without data source lookup.

        Returns:
            Iterable of records with the same length and in the same order as the list of keys.
            A result element is None if the record is not found or the key is None.

        Args:
            records_or_keys: Each element is a record, key in tuple format, or None.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
            context: Optional context, if None current context will be used
        """
        # TODO: Does not yet support embedded keys

        # Handle empty input
        if len(records_or_keys) == 0:
            return []

        # Assign codes to input elements
        coded_inputs = [
            (_NONE, x)
            if x is None
            else (_KEY, x)
            if isinstance(x, tuple) and len(x) > 0 and isinstance(x[0], type) and issubclass(x[0], cls)
            else (_RECORD, x)
            if isinstance(x, cls)
            else (_UNKNOWN, x)
            for x in records_or_keys
        ]

        # Check for unknown input types
        unknown_inputs = [x[1] for x in coded_inputs if x[0] == _UNKNOWN]
        if len(unknown_inputs) > 0:
            unknown_types = [str(type(x).__name__) for x in unknown_inputs[:5]]
            unknown_types_str = ", ".join(unknown_types)
            raise RuntimeError(
                f"Elements of `records_or_keys` param in `load_many` can be objects of "
                f"class {cls.__name__} or its subclass, tuple where the first element "
                f"is the type of this class or its subclass, or None. The following "
                f"parameter types are not accepted by this method: {unknown_types_str}"
            )

        # Keys without preserving position in list, excludes None
        keys = [x[1] for x in coded_inputs if x[0] == _KEY]

        if len(keys) == 0:
            # If there are no keys, return a copy of the input list and stop further processing
            return list(records_or_keys)

        # Get data source from the current or specified context
        context = Context.current() if context is None else context
        data_source = context.data_source()
        base_type = cls.get_base_type()

        # Each lookup must not exceed data source batch size
        batch_size = data_source.batch_size()
        batches = [keys[i : i + batch_size] for i in range(0, len(keys), batch_size)]
        records_dict = {}
        for batch_keys in batches:
            # Get unordered dict of serialized record data
            batch_data = data_source.load_unordered(batch_keys, dataset)

            # Create class instances and accumulate in records_dict, key[0] is type
            records_dict.update({key: key[0](**dict_) for key, dict_ in batch_data})

        # Replace key by record defaulting to None, otherwise return input record or None
        result = [records_dict.get(x[1], None) if x[0] == _KEY else x[1] for x in coded_inputs]
        return result
