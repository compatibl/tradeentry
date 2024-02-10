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

from enum import IntEnum


class VariantType(IntEnum):
    """Enumeration for the atomic value type."""

    Empty = 0
    """
    Indicate that enum value is not set.

    In programming languages where enum defaults to the first item when
    not set, making Empty the first item prevents unintended assignment
    of a meaningful value.
    """

    String = 1
    """String value."""

    Double = 2
    """Double value."""

    Bool = 3
    """Boolean value."""

    Int = 4
    """32-bit integer value."""

    Long = 5
    """64-bit long value."""

    Date = 6
    """Local date without the time component (does not specify timezone)."""

    Time = 7
    """Local time without the date component to one millisecond resolution (does not specify timezone)."""

    DateTime = 9
    """Local datetime to one millisecond resolution (does not specify timezone)."""  # TODO: Value of 8 is skipped

    Enum = 11
    """Enumeration."""

    Key = 12
    """Key."""

    Data = 13
    """Data."""
