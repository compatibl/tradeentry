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


class AtomicType(IntEnum):
    """List of values and immutable types, including string and binary."""

    Bool = 0
    """Bool value."""

    Int = 1
    """Int value."""

    Long = 2
    """Long value."""

    Double = 3
    """Double value."""

    Date = 4
    """Date value."""

    DateTime = 5
    """DateTime value."""

    String = 6
    """String value."""

    Binary = 7
    """Binary value."""

    Key = 8
    """Key value."""

    Data = 9
    """Generic data value."""

    Variant = 10
    """Variant value."""

    Decimal = 11
    """Decimal value."""

    Time = 12
    """Time value."""

    Guid = 13
    """Guid value."""

    InstantTime = 14
    """InstantTime value."""

    Query = 15
    """Query value."""

    @classmethod
    def custom_labels(cls):
        """Custom enum item labels dict."""

        return {cls.DateTime: "DateTime", cls.InstantTime: "InstantTime"}
