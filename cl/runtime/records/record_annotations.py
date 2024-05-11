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
from typing import Any, Iterable, List, TypeVar
from typing import Dict
from typing import Literal
from typing import Tuple
from typing import Type

GenericKey = Tuple[
    Type,  # First element is the record's type
    ...,  # Remaining elements are primary key fields in the order of declaration
]
"""Tuple of (type, primary key fields)."""

GenericValue = str | float | bool | int | dt.date | dt.time | dt.datetime
"""Primitive value fields."""

GenericField = Dict[str, "GenericField"] | List["GenericField"] | GenericValue
"""Primitive value fields and data containers."""

GenericData = Dict[str, GenericField]
"""Serialized record data in dictionary format (other formats may be added in the future)."""

GenericIdentity = str
"""Identity string (other formats may be added in the future)."""

GenericTimestamp = dt.datetime
"""Timestamp in datetime format (time ordered, globally unique formats may be added in the future)."""

GenericPack = Tuple[
    GenericKey,  # Tuple of (type, primary key fields)
    GenericData,  # Serialized record data in dictionary format (other formats may be added in the future)
]
"""
Tuple of (KEY, DATA) where:
    - KEY: A tuple of (type, primary key fields)
    - DATA: Serialized record data in dictionary format (other formats may be added in the future)
"""

GenericRecord = Tuple[
    GenericKey,  # Tuple of (type, primary key fields)
    GenericData,  # Serialized record data in dictionary format (other formats may be added in the future)
    GenericIdentity,  # Identity data used for row level security
    Iterable[str] | None,  # Record's dataset as a list of path tokens (empty list or None means root dataset)
    GenericTimestamp,  # Timestamp for the time the record was written to storage
]
"""
Tuple of (KEY, DATA, IDENTITY, DATASET, TIMESTAMP) where:
    - KEY: A tuple of (type,primary key fields)
    - DATA: Serialized record data in dictionary format (other formats may be added in the future)
    - IDENTITY: Identity data used for row level security
    - DATASET: Record's dataset as a list of path tokens (empty list or None means root dataset)
    - TIMESTAMP: Timestamp for the time the record was written to storage
"""

GenericQuery = Tuple[
    Type,  # Query type and its descendents will be returned by the query. It must include all query and order fields.
    Dict[str, Any],  # NoSQL query conditions in MongoDB format.
    Dict[str, Literal[1, -1]],  # NoSQL query order in MongoDB format.
]
"""NoSQL query data in MongoDB format."""
