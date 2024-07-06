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

from typing import Protocol, Any, Type


def is_record(type_or_obj: Any) -> bool:
    """
    Check if type or object is a record based on the presence of 'get_key' attribute
    without requiring inheritance from RecordMixin.
    """
    return hasattr(type_or_obj, "get_key")


def is_key(type_or_obj: Any) -> bool:
    """
    Check if type or object is a key (but not a record derived from key) based on the presence of 'get_key_type'
    attribute and the absence of 'get_key' attribute, without requiring inheritance from KeyMixin.
    """
    return hasattr(type_or_obj, "get_key_type") and not hasattr(type_or_obj, "get_key")


class KeyProtocol(Protocol):
    """Protocol implemented by both keys and records (which are derived from keys)."""

    def get_key_type(self) -> Type:
        """Type of the key object determines the table."""


class RecordProtocol(KeyProtocol):
    """Protocol implemented by records but not keys."""

    def get_key(self) -> KeyProtocol:
        """Return key object for the current record."""
