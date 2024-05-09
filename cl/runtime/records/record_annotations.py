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

from typing import Any
from typing import Dict
from typing import Tuple
from typing import Type

KeyType = Tuple[
    Type,               # First element is the record's type
    ...                 # Remaining elements are primary key fields in the order of declaration
]
"""Tuple of (type, primary key fields)."""

DataType = Dict[str, Any]
"""Serialized record data."""

PackType = Tuple[
    KeyType,            # Tuple of (type, primary key fields)
    DataType            # Record data serialized into a dictionary
]
"""Tuples of (KEY,DICT) where KEY=(type,primary key fields) and DICT contains serialized record data."""
