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
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Literal
from typing import Tuple
from typing import Type
from typing import TypeVar

TKey = Tuple[
    Type,  # First element is the record's type
    ...,  # Remaining elements are primary key fields in the order of declaration
]
"""Tuple of (type, primary key fields)."""

TPrimitive = str | float | bool | int | dt.date | dt.time | dt.datetime
"""Primitive value fields."""

TField = Dict[str, "TField"] | List["TField"] | TPrimitive
"""Primitive value fields and data containers."""

TData = Dict[str, TField]
"""Serialized record data in dictionary format (other formats may be added in the future)."""

TIdentity = str
"""Identity string (other formats may be added in the future)."""

TDataset = Iterable[str] | None
"""Dataset as a list of tokens, a backslash-delimited string starting from backslash, or None."""

TStamp = dt.datetime
"""Timestamp or time-ordered globally unique identifier."""

TPack = Tuple[
    TKey,  # Tuple of (type, primary key fields)
    TData,  # Serialized record data in dictionary format (other formats may be added in the future)
]
"""
Tuple of (TKey, TData) where:
    - TKey: A tuple of (type, primary key fields)
    - TData: Serialized record data in dictionary format (other formats may be added in the future)
"""

TRecord = Tuple[
    TKey,  # Tuple of (type, primary key fields)
    TData,  # Serialized record data in dictionary format (other formats may be added in the future)
    TIdentity,  # Identity token used for row level security
    TDataset,  # Record's dataset as a list of path tokens (empty list or None means root dataset)
    TStamp,  # Timestamp or time-ordered globally unique identifier
]
"""
Tuple of (TKey, TData, TIdentity, TDataset, TStamp) where:
    - TKey: A tuple of (type, primary key fields)
    - TData: Serialized record data in dictionary format (other formats may be added in the future)
    - TIdentity: Identity token used for row level security
    - TDataset: Dataset as a list of tokens, a backslash-delimited string starting from backslash, or None.
    - TStamp: Timestamp for the time the record was written to storage
"""

TQuery = Tuple[
    Type,  # Query type and its descendents will be returned by the query. It must include all query and order fields.
    Dict[str, Any],  # NoSQL query conditions in MongoDB format.
    Dict[str, Literal[1, -1]],  # NoSQL query order in MongoDB format.
]
"""NoSQL query data in MongoDB format."""
