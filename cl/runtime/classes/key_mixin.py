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
from typing import Dict, Any, List, TypeVar, Type, Literal

from cl.runtime.classes.class_info import ClassInfo
from cl.runtime.classes.data_mixin import DataMixin
from typing_extensions import Self
from cl.runtime.rest.context import Context

# Generic parameter for the key and record types
TKey = TypeVar('TKey', bound='KeyMixin', covariant=False, contravariant=False)
TRecordOrKey = TypeVar('TRecordOrKey', bound='KeyMixin', covariant=True, contravariant=False)

# Key format type
KeyFormat = Literal["record", "key", "dict", "str", "unknown"]


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

    @classmethod
    def to_str_key(cls: Type[TRecordOrKey], record_or_key: TRecordOrKey | dict | str | None) -> str | None:
        """
        Key as string in semicolon-delimited string format without table name.

        For composite keys, the embedded keys are concatenated in the order of their declaration without brackets:

            - No primary key fields: '' (i.e. empty string)
            - One primary key field A: 'A'
            - Two primary key fields A and B: 'A;B'
            - Two primary key fields 'A1;A2' and 'B': 'A1;A2;B'
        """
        if record_or_key is None:
            return None
        elif isinstance(record_or_key, str):
            return record_or_key
        elif isinstance(record_or_key, dict):
            raise NotImplementedError()
        elif type(record_or_key).__name__.endswith("Key") or isinstance(record_or_key, cls):
            pass
        else:
            raise RuntimeError(
                f"Wrong parameter type {type(record_or_key).__name__} for converting class {cls.__name__} "
                f"to string key."
            )

    @classmethod
    def to_dict_key(cls: Type[TRecordOrKey], record_or_key: TRecordOrKey | dict | str | None) -> Dict[str, Any] | None:
        """Return key as a dict of primary key fields."""
        if False:  # TODO: Implement
            return None
        else:
            raise RuntimeError(
                f"Wrong parameter type {type(record_or_key).__name__} for converting class {cls.__name__} "
                f"to dict key."
            )

    @classmethod
    def to_generic_key(cls: Type[TRecordOrKey], record_or_key: TRecordOrKey | dict | str | None) -> str | None:
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
        raise NotImplementedError()

    def __repr__(self) -> str:
        """
        Key as string in semicolon-delimited string format without table name.

        Notes:
            This method is for debugging purposes only and may be overridden in derived types. Do not use in code.
        """
        return type(self).to_str_key(self)

    @classmethod
    def load_many(
            cls,
            key_type_or_table: Type[TKey] | str,
            records_or_keys: List[Self | None] | List[TKey | None] | List[dict | None] | List[str | None] | None,
            dataset: List[str] | str | None = None,
            *,
            context: Context = None
    ) -> List[Self | None] | None:
        """
        Load serialized records from a single table using a list of keys.
        If records are passed instead of keys, they are returned without data source lookup.

        Returns:
            Iterable of records with the same length and in the same order as the list of keys.
            A result element is None if the record is not found or the key is None.

        Args:
            key_type_or_table: Type of key class or table name as string
            records_or_keys: Each element is a record, key, semicolon-delimited string, or None.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
            context: Optional context, if None current context will be used
        """

        # TODO: Check - This method should not be called for a key class

        # Return None if `records_or_keys` is empty or None
        if records_or_keys is None or len(records_or_keys) == 0:
            return None

        # If `records_or_keys` is List[None], return List[None] of the same length
        if all(x is None for x in records_or_keys):
            return [] * len(records_or_keys)

        # Create a list of key formats
        key_formats: List[str] = [
            "str" if isinstance(x, str) else
            "dict" if isinstance(x, dict) else
            "key" if type(x).__name__.endswith("Key") else
            "record" if isinstance(x, cls)  else
            f"unknown.{type(x).__name__}"
            for x in records_or_keys if x is not None
        ]

        # Eliminate duplicates
        key_formats = list(set(key_formats))

        # Check if there are any unknown types
        unknown = [x.removeprefix("unknown.") for x in key_formats if x.startswith("unknown.")]
        if len(unknown) > 0:
            # Report the first 10 unknown types
            desc = ", ".join(unknown[:10])
            raise RuntimeError(f"Param `records_or_keys` of method `load_many` can only contain the following "
                               f"types: record derived from `{cls.__name__}`, key, dict, or string. "
                               f"These types are not supported: {desc}.")

        # Determine format, error message if more than one is present
        if len(key_formats) > 1:
            # More than one key format, report
            desc = ", ".join(key_formats)
            raise RuntimeError(f"Param `records_or_keys` of method `load_many` can only contain one key format "
                               f"but contains {len(key_formats)}: {desc}.")
        elif len(key_formats) == 1:
            # One key format, use
            key_format = key_formats[0]
        else:
            # Should not happen with the current version of the code above, handling as a precaution
            raise RuntimeError("The size of key formats list is zero.")

        # Handle record type first
        if key_format == "record":

            # Return a copy of `records_or_keys`
            return list(records_or_keys)

        else:

            # Determine table name
            table: str
            if isinstance(key_type_or_table, type):
                # Type of key class
                key_class_name = key_type_or_table.__name__
                if key_class_name.endswith("Key"):
                    table = key_class_name.removesuffix("Key")
                else:
                    raise RuntimeError(f"Invalid value `{key_class_name}` of `key_type_or_table` parameter, "
                                       f"if type rather than string is specified the type name must end with `Key`.")
            elif isinstance(key_type_or_table, str):
                # String, use directly
                table = key_type_or_table
            else:
                raise RuntimeError(f"Invalid type `{type(key_type_or_table)}` of `key_type_or_table` parameter, "
                                   f"must be either string or type of the key class.")

            # Get data source from the current or specified context
            context = Context.current() if context is not None else context
            data_source = context.data_source()

            # Only load those keys that are not none
            loaded_keys = [x for x in records_or_keys if x is not None]

            # Convert to the key format required by the data source
            required_format = data_source.key_format()
            if required_format == 'dict':
                if key_format != "dict":
                    loaded_keys = [cls.to_dict_key(k) for k in loaded_keys]
            elif required_format == 'str':
                if key_format != "str":
                    loaded_keys = [cls.to_str_key(k) for k in loaded_keys]
            else:
                raise RuntimeError(f"Key format `{required_format}` required by data source "
                                   f"`{data_source.data_source_id}` is not supported.")

        # Each lookup must not exceed data source batch size
        batch_size = data_source.batch_size()
        batches = [loaded_keys[i:i + batch_size] for i in range(0, len(loaded_keys), batch_size)]
        loaded_records = {}
        for batch_keys in batches:

            # Get unordered list of serialized records in dict format
            batch_dicts = data_source.load_unordered(table, batch_keys, dataset)

            # Create classes from serialized dicts
            batch_records: List[Self] = [ClassInfo.from_dict(x) for x in batch_dicts]

            # Add classes to dict
            loaded_records.update({cls.to_str_key(x): x for x in batch_records})

        # Convert elements of `records_or_keys` to string except when they are None
        str_keys = [cls.to_str_key(k) for k in records_or_keys] if key_format != str else list(records_or_keys)

        # Replace string keys by lookup from `loaded_records`, default to None if not found
        result = [loaded_records.get(x, None) if x is not None else None for x in str_keys]
        return result
