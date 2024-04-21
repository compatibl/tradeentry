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

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from cl.runtime.rest.context import Context
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing_extensions import Self

NONE = 0  # Code indicating None
KEY = 1  # Code indicating tuple
RECORD = 2  # Code indicating record
UNKNOWN = 3  # Code indicating unknown type


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
    def get_key(self) -> Tuple[Type, ...]:
        """Return a tuple starting from the base record class followed by the primary key fields."""

    @abstractmethod
    def pack(self) -> Tuple[Tuple[Type, ...], Type[Self], Dict[str, Any]]:
        """Return a tuple of containing the record's key, class, and data serialized into a dictionary."""

    def init(self) -> None:
        """Similar to __init__ but uses previously set fields instead of parameters (not invoked by data source)."""

        # Do nothing by default
        pass

    def validate(self) -> None:
        """Validate previously set fields (invoked by data source before saving and after loading)."""

        # Do nothing by default
        pass

    @classmethod
    def load_many(
        cls,
        records_or_keys: List[Self | Tuple | None],
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
            (NONE, x)
            if x is None
            else (KEY, x)
            if isinstance(x, tuple)
            else (RECORD, x)
            if isinstance(x, cls)
            else (UNKNOWN, x)
            for x in records_or_keys
        ]

        # Check for unknown input types
        unknown_inputs = [x[1] for x in coded_inputs if x[0] == UNKNOWN]
        if len(unknown_inputs) > 0:
            unknown_types = [str(type(x).__name__) for x in unknown_inputs[:5]]
            unknown_types_str = ", ".join(unknown_types)
            raise RuntimeError(
                f"Param `records_or_keys` of method `load_many` can have elements "
                f"of type {cls.__name__}, tuple, or None. The following "
                f"parameter types are invalid: {unknown_types_str}"
            )

        # Keys without preserving position in list, excludes None
        keys = [x[1] for x in coded_inputs if x[0] == KEY]

        if len(keys) == 0:
            # If there are no keys, return a copy of the input list and stop further processing
            return list(records_or_keys)

        # Get data source from the current or specified context
        context = Context.current() if context is None else context
        data_source = context.data_source()

        # Each lookup must not exceed data source batch size
        batch_size = data_source.batch_size()
        batches = [keys[i : i + batch_size] for i in range(0, len(keys), batch_size)]
        records_dict = {}
        for batch_keys in batches:
            # Get unordered dict of serialized record data
            batch_data = data_source.load_unordered(batch_keys, dataset)  # noqa

            # Create class instances and accumulate in records_dict
            records_dict.update({key: type_(**dict_) for key, type_, dict_ in batch_data})

        # Replace key by record defaulting to None, otherwise return input record or None
        result = [records_dict.get(x[1], None) if x[0] == KEY else x[1] for x in coded_inputs]
        return result
