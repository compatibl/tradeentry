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
from typing_extensions import Self
from typing import Any, Dict, Optional
from cl.runtime import Data


class StubCustomData(Data):
    """Stub serializable data used in tests."""

    base_field_str: Optional[str]
    """String attribute of base class."""

    base_field_int: Optional[int]
    """Float attribute of base class."""

    def __init__(self, *,
                 base_field_str: str = 'abc',
                 base_field_int: int = 123
                 ):
        """Initialize instance attributes."""
        self.base_field_str = base_field_str
        self.base_field_int = base_field_int

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary containing other dictionaries, lists and primitive types."""
        return {
            'base_field_str': self.base_field_str,
            'base_field_int': self.base_field_int,
        }

