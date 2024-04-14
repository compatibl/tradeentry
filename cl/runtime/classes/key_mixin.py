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
from typing import Dict, Any, List, TypeVar, Type, Literal, get_type_hints

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
    def to_str_key(cls, key_type: Type[TKey], record_or_key: Self | TKey | dict | str | None) -> str | None:
        """
        Convert all key formats to semicolon-delimited string without table name.

        Notes:
            For composite keys, the embedded keys are concatenated in the order of their declaration without brackets:

                - No primary key fields: '' (i.e. empty string)
                - One primary key field A: 'A'
                - Two primary key fields A and B: 'A;B'
                - Two primary key fields 'A1;A2' and 'B': 'A1;A2;B'

        Returns:
            Key as string in semicolon-delimited string format without table name.

        Args:
            key_type: Type of key class.
            record_or_key: Record, key, dict, semicolon-delimited string, or None.
        """
        if record_or_key is None:
            return None
        elif isinstance(record_or_key, str):
            return record_or_key
        elif isinstance(record_or_key, dict):
            field_types = get_type_hints(key_type)
            if len(record_or_key) != len(field_types):
                dict_keys = record_or_key.keys()
                dict_keys_desc = ", ".join(f"`{dict_keys}`")
                field_names = field_types.keys()
                key_fields_desc = ", ".join(f"`{field_names}`")
                raise RuntimeError(f"Dict key {record_or_key} has {len(dict_keys)} tokens for key type "
                                   f"{key_type.__name__} which has {len(field_names)} fields. "
                                   f"Dict keys: {dict_keys_desc}. Key fields: {key_fields_desc}.")
            tokens = [record_or_key[x] for x in field_types]
            result = ";".join(tokens)
            return result
        elif record_or_key is key_type or isinstance(record_or_key, cls):
            field_types = get_type_hints(key_type)
            tokens = [str(getattr(record_or_key, x)) for x in field_types]
            result = ";".join(tokens)
            return result
        else:
            raise RuntimeError(
                f"Wrong parameter type `{type(record_or_key).__name__}` for converting class `{cls.__name__}` "
                f"to string key."
            )

    @classmethod
    def to_dict_key(cls, key_type: Type[TKey], record_or_key: Self | TKey | dict | str | None) -> Dict[str, Any] | None:
        """
        Convert all key formats to key dict.

        Notes:
            For composite keys, the embedded keys are represented as embedded dicts.

        Returns:
            Dict of key fields.

        Args:
            key_type: Type of key class.
            record_or_key: Record, key, dict, semicolon-delimited string, or None.
        """

        if record_or_key is None:
            return None
        elif isinstance(record_or_key, str):
            # Use field names as keys and tokens as values
            field_types = get_type_hints(key_type)
            field_names = field_types.keys()
            tokens = record_or_key.split(";")
            if len(tokens) != len(field_names):
                key_fields_desc = ", ".join(f"`{field_names}`")
                raise RuntimeError(f"String key `{record_or_key}` has {len(tokens)} tokens for key type "
                                   f"`{key_type.__name__}` which has {len(field_names)} fields: {key_fields_desc}")
            result = dict(zip(field_names, tokens))
            return result
        elif isinstance(record_or_key, dict):
            # Create a copy
            return dict(record_or_key)
        elif record_or_key is key_type or isinstance(record_or_key, cls):
            field_types = get_type_hints(key_type)
            result = {x: getattr(record_or_key, x) for x in field_types}
            return result
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

    def __str__(self) -> str:
        """
        Key as string in semicolon-delimited string format without table name.

        Notes:
            This method is for debugging purposes only and may be overridden in derived types. Do not use in code.
        """
        class_type = type(self)  # TODO: Support calling this method for types derived from key
        return class_type.to_str_key(class_type, self)

    @classmethod
    def load_many(
            cls,
            key_type: Type[TKey],
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
            key_type: Type of key class.
            records_or_keys: Each element is a record, key, semicolon-delimited string, or None.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
            context: Optional context, if None current context will be used
        """

        # TODO: Does not yet support embedded keys

        # This method should not be called for the key class
        if cls == key_type:
            raise RuntimeError(f"Method `load_many` should not be called for the key class {key_type.__name__}")

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
            "key" if x is key_type else
            "record" if isinstance(x, cls) else
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
                               f"types: str, dict, `{key_type.__name__}`, or any class derived from `{cls.__name__}`. "
                               f"The following types are not supported: {desc}.")

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

            # Determine table name, use key_type with removed Key suffix if present
            table = key_type.removesuffix("Key")

            # Get data source from the current or specified context
            context = Context.current() if context is not None else context
            data_source = context.data_source()

            # Only load those keys that are not none
            loaded_keys = [x for x in records_or_keys if x is not None]

            # Convert to the key format required by the data source
            required_format = data_source.key_format()
            if required_format == 'dict':
                if key_format != "dict":
                    loaded_keys = [cls.to_dict_key(key_type, k) for k in loaded_keys]
            elif required_format == 'str':
                if key_format != "str":
                    loaded_keys = [cls.to_str_key(key_type, k) for k in loaded_keys]
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
