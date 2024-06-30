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


from cl.runtime.context.context import Context
from cl.runtime.storage.data_source_types import TDataset, TLoadedRecord
from cl.runtime.storage.data_source_types import TIdentity
from cl.runtime.storage.data_source_types import TKey
from typing import Iterable
from typing import List
from typing import Type
from typing import TypeVar

_NONE = 0  # Code indicating None
_KEY = 1  # Code indicating a key in tuple format
_UNKNOWN = 3  # Code indicating unknown type

TObj = TypeVar("TObj", bound="RecordUtil")


class RecordUtil:
    """Static helper class for RecordMixin."""

    def __init__(self):
        """Prevent instance creation."""
        raise RuntimeError(f"{self.__class__.__name__} is a static helper class, no instances are necessary.")

    @staticmethod
    def load_many(
        record_type: Type[TObj],
        records_or_keys: List[TObj | TKey | None],
        *,
        context: Context | None = None,
        dataset: TDataset = None,
    ) -> List[TObj | None]:
        """
        Load serialized records from a single table using a list of keys.

        Returns:
            Iterable of records with the same length and in the same order as the list of keys.
            The result element is None if the record is not found or the key is None.

        Args:
            record_type: Type to which loaded records will be cast
            keys: List where each element is a key or None
            context: Optional context, if None current context will be used
            dataset: Lookup dataset as a delimited string, list of levels, or None
        """

        # Handle empty input
        if len(records_or_keys) == 0:
            return []

        # Assign codes to input elements
        coded_inputs = [
            (_NONE, x)
            if x is None
            else (_KEY, x)
            if type(x).__name__.endswith("Key")  # TODO: Support short names
            else (_UNKNOWN, x)
            for x in records_or_keys
        ]

        # Check for unknown input types
        unknown_inputs = [x[1] for x in coded_inputs if x[0] == _UNKNOWN]
        if len(unknown_inputs) > 0:
            unknown_types = [str(type(x).__name__) for x in unknown_inputs[:5]]
            unknown_types_str = ", ".join(unknown_types)
            raise RuntimeError(
                f"Elements of `records_or_keys` param in `load_many` can be keys in "
                f"tuple format where the first element is a type or None. The following "
                f"parameter types are not accepted by this method: {unknown_types_str}"
            )

        # Keys without preserving position in list, excludes None
        keys: List[TKey] = [x[1] for x in coded_inputs if x[0] == _KEY]  # noqa

        if len(keys) == 0:
            # If there are no keys, each element is None.
            # In this case we can return a list of None of
            # the same size without further processing
            return list(records_or_keys)

        # Get data source from the current or specified context
        context = Context.current() if context is None else context
        data_source = context.data_source()

        # Each lookup must not exceed data source batch size
        batch_size = data_source.batch_size()
        batches = [keys[i : i + batch_size] for i in range(0, len(keys), batch_size)]
        records_dict = {}
        for batch_keys in batches:

            # Get unordered dict of record data serialized as (record_type, serialized_data) tuple
            record_tuples: Iterable[TLoadedRecord] = data_source.load_many(batch_keys, dataset=dataset)

            # Create class instances and accumulate in records_dict
            records_dict.update({key.get_generic_key(): data[0](**data[1]) for key, data, dataset, stamp in record_tuples})

        # Replace key by record defaulting to None, otherwise return input record or None
        result = [records_dict.get(x[1].get_generic_key(), None) if x[0] == _KEY else x[1] for x in coded_inputs]
        return result
