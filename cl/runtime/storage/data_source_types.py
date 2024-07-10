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
import uuid
from enum import Enum
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Literal
from typing import Tuple
from typing import Type

TPrimitive = str | float | bool | int | dt.date | dt.time | dt.datetime | uuid.UUID | bytes
"""Supported primitive value types for serialized data in dictionary format."""

TDataField = Dict[str, "TDataField"] | List["TDataField"] | TPrimitive | Enum | None
"""Supported field types for serialized data in dictionary format."""

TDataDict = Dict[str, TDataField]
"""Serialized data in dictionary format."""

TKeyField = Dict[str, "TKeyField"] | TPrimitive | Enum
"""Supported field types for serialized key in dictionary format."""

TKeyDict = Dict[str, TKeyField]
"""Serialized key in dictionary format."""

TIdentity = str | None
"""Identity token used for row level security."""

TDataset = Iterable[str] | None
"""Dataset as a delimited string, list of levels, or None."""

TStamp = dt.datetime | uuid.UUID | None
"""Timestamp or time-ordered globally unique identifier in UUID7 format."""  # TODO: Confirm UUID format to use

TQuery = Tuple[
    Type,  # Query type and its descendents will be returned by the query. It must include all query and order fields.
    Dict[str, Any],  # NoSQL query conditions in MongoDB format.
    Dict[str, Literal[1, -1]],  # NoSQL query order in MongoDB format.
]
"""NoSQL query data in MongoDB format."""
