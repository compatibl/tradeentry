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

import datetime as dt
from enum import Enum
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Literal
from typing import Tuple
from typing import Type
from typing import TypeVar
from uuid import UUID

TKey = Tuple[
    Type,  # First element is the table type
    ...,  # Remaining elements are primary key fields of TPrimitive type in the order of declaration
]
"""Tuple in (table_type, primary_key_1, primary_key_2, ...) format."""

# TODO: Add type as a primitive value
TPrimitive = str | float | bool | int | dt.date | dt.time | dt.datetime | UUID | bytes
"""Supported primitive value types in serialized data."""

# TODO: Remove Enum
TField = Dict[str, "TField"] | List["TField"] | TKey | TPrimitive | Enum | None
"""Supported field types in serialized data."""

TData = Tuple[
    Type,  # Class holding the data after deserialization
    Dict[str, TField],  # Serialized record data in dictionary format (other formats may be added in the future)
]
"""Serialized data in dictionary format (other formats may be added in the future)."""

TIdentity = str | None
"""Identity token used for row level security."""

TDataset = Iterable[str] | None
"""Dataset as a delimited string, list of levels, or None."""

TStamp = dt.datetime | UUID
"""Timestamp or time-ordered globally unique identifier in UUID7 format."""  # TODO: Confirm UUID format to use

TPackedRecord = Tuple[
    TKey,  # Tuple in (table_type, primary_key_1, primary_key_2, ...) format
    TData,  # Serialized record data in dictionary format (other formats may be added in the future)
]
"""
Tuple of (Type, TKey, TData) where:
    - Type: Class to which the record is deserialized
    - TKey: Tuple in (table_type, primary_key_1, primary_key_2, ...) format
    - TData: Serialized record data in dictionary format (other formats may be added in the future)
"""

TLoadedRecord = Tuple[
    Type,  # Class to which the record is deserialized
    TKey,  # Tuple in (table_type, primary_key_1, primary_key_2, ...) format
    TData,  # Serialized record data in dictionary format (other formats may be added in the future)
    TDataset,  # Record's dataset as a delimited string, list of levels, or None
    TStamp,  # Timestamp or time-ordered globally unique identifier
]
"""
Tuple of (Type, TKey, TData, TIdentity, TDataset, TStamp) where:
    - Type: Class to which the record is deserialized
    - TKey: Tuple in (table_type, primary_key_1, primary_key_2, ...) format
    - TData: Serialized record data in dictionary format (other formats may be added in the future)
    - TDataset: Record's dataset as a delimited string, list of levels, or None
    - TStamp: Timestamp for the time the record was written to storage
"""

TSavedRecord = Tuple[
    Type,  # Class to which the record is deserialized
    TKey,  # Tuple in (table_type, primary_key_1, primary_key_2, ...) format
    TData,  # Serialized record data in dictionary format (other formats may be added in the future)
    TDataset,  # Record's dataset as a delimited string, list of levels, or None
    TStamp,  # Timestamp or time-ordered globally unique identifier
    TIdentity,  # Identity token used for row level security.
]
"""
Tuple of (Type, TKey, TData, TIdentity, TDataset, TStamp) where:
    - Type: Class to which the record is deserialized
    - TKey: Tuple in (table_type, primary_key_1, primary_key_2, ...) format
    - TData: Serialized record data in dictionary format (other formats may be added in the future)
    - TDataset: Record's dataset as a delimited string, list of levels, or None
    - TStamp: Timestamp for the time the record was written to storage
    - TIdentity: Identity token used for row level security
"""

TQuery = Tuple[
    Type,  # Query type and its descendents will be returned by the query. It must include all query and order fields.
    Dict[str, Any],  # NoSQL query conditions in MongoDB format.
    Dict[str, Literal[1, -1]],  # NoSQL query order in MongoDB format.
]
"""NoSQL query data in MongoDB format."""
