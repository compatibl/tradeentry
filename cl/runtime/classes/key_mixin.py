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
from typing import Dict, Any, Iterable, List

from cl.runtime.classes.data_mixin import DataMixin
from typing_extensions import Self

from cl.runtime.classes.record_mixin import RecordMixin
from cl.runtime.rest.context import Context


class KeyMixin(DataMixin, ABC):
    """
    Optional mixin class for database keys providing static type checkers with method signatures.

    Those methods that raise an exception must be overridden in derived types or by a decorator.
    They are not made abstract to avoid errors from static type checkers.

    The use of this class is optional. The code must not rely on inheritance from this class.
    """

    __slots__ = []  # Adding an empty __slots__ declaration prevents the creation of a __dict__ for every instance

    def get_table(self) -> str:
        """
        Name of the database table where the record for this key is stored.

        By convention, table name consists of a namespace (full package path or short alias)
        followed by the dot delimiter and then the class name of the common base to all records
        stored in the table: 'namespace.RecordType'
        """
        raise RuntimeError(
            f"Method get_table() for class {type(self).__name__} in module {type(self).__module__} "
            f"is neither implemented in code nor by a decorator."
        )

    def get_key(self) -> str:
        """
        Key as string in semicolon-delimited string format without table name.

        For composite keys, the embedded keys are concatenated in the order of their declaration without brackets:

            - No primary key fields: '' (i.e. empty string)
            - One primary key field A: 'A'
            - Two primary key fields A and B: 'A;B'
            - Two primary key fields 'A1;A2' and 'B': 'A1;A2;B'
        """
        raise RuntimeError(
            f"Method get_key() for class {type(self).__name__} in module {type(self).__module__} "
            f"is neither implemented in code nor by a decorator."
        )

    def dict_key(self) -> Dict[str, Any]:
        """Return key as a dict of primary key fields."""
        raise RuntimeError(
            f"Method dict_key() for class {type(self).__name__} in module {type(self).__module__} "
            f"is neither implemented in code nor by a decorator."
        )

    def get_generic_key(self) -> str:
        """
        Generic key string defines both the table and the record within the table. It consists of the
        table name followed by the primary key in semicolon-delimited string format.

        By convention, table name consists of a namespace (full package path or short alias) followed by
        the class name of the common base to all classes stored in the table with dot delimiter:

        - No primary key fields: 'namespace.RecordType'
        - One primary key field A: 'namespace.RecordType;A'
        - Two primary key fields A and B: 'namespace.RecordType;A;B'
        - Two primary key fields 'A1;A2' and 'B': 'namespace.RecordType;A1;A2;B'
        """
        return f"{self.get_table()};{self.get_key()}"

    def __str__(self) -> str:
        """
        Key as string in semicolon-delimited string format without table name.

        This method is for debugging purposes only and may be overridden to return additional data.
        Data source implementation must use get_key() method instead.
        """
        return self.get_key()

    @classmethod
    def load_many(
            cls,
            records_or_keys: List[Self | str | None],
            dataset: List[str] | str | None = None,
            *,
            context: Context = None
    ) -> List[Self | None]:
        """
        Load serialized records from a single table using a list of keys.
        If a record is passed instead of a key, the record is returned without data source lookup.

        Returns:
            Iterable of records with the same length and in the same order as the list of keys.
            A result element is None if the record is not found or the key is None.

        Args:
            records_or_keys: Each element is a record, key, semicolon-delimited string, or None.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
            context: Optional context, if None current context will be used
        """

        key_class_name = cls.__name__
        if key_class_name.endswith("Key"):
            table = key_class_name.removesuffix("Key")
        else:
            raise RuntimeError(f"An implementation of `load_many` for key classes was called "
                               f"for class {key_class_name} whose name does not end with `Key`.")

        context = Context.current() if context is not None else context
        data_source = context.data_source()

        # Check for the presence of unrelated types
        unrelated = [x for x in records_or_keys if not (isinstance(x, cls) or isinstance(x, str) or x is None)]
        if unrelated:
            raise RuntimeError(f"Unrelated type `{type(unrelated[0])}` is passed to `load_many` "
                               f"method for key class `{cls.__name__}`.")

        # Keys are strings or have the exact type cls (any derived type is assumed to be a record).
        # Because other elements are excluded, the resulting array may have smaller size than `records_or_keys`
        keys = [x for x in records_or_keys if x is not None and (isinstance(x, str) or type(x) is cls)]

        # Convert keys to the required format
        key_format = data_source.key_format()
        if key_format == 'dict':
            # Required key format is dict
            keys = [k if not isinstance(k, str) else k.dict_key() for k in keys]
        elif key_format == 'str':
            # Required key format is str
            keys = [k if isinstance(k, str) else k.str_key() for k in keys]
        else:
            raise RuntimeError(f"Unsupported key format `{key_format}` in data source `{data_source.data_source_id}`.")

        # Populate with records or strings first
        records = [
            x if x is None or isinstance(x, str) or (isinstance(x, cls) and type(x) is not cls) else x.str_key()
            for x in records_or_keys
        ]

        # Each lookup must not exceed data source batch size
        loaded_records = {}
        keys_size = len(keys)
        batch_size = data_source.batch_size()
        batches = [keys[i:i + batch_size] for i in range(0, keys_size, batch_size)]
        for batch_keys in batches:

            # Get unordered list of serialized records in dict format
            batch_dicts = data_source.load_unordered(table, batch_keys, dataset)

            # Create classes from serialized dicts
            batch_records: List[Self] = []

            # Add classes to dict
            loaded_records.update({x.str_key(): x for x in batch_records})

        # Replace string elements by lookup from `loaded_records`, default to None if not found
        result = [loaded_records.get(x, None) if isinstance(x, str) else x for x in records]
        return result
