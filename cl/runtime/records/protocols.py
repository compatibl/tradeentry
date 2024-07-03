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

from typing import Protocol, Tuple, Any


def is_record(type_or_obj: Any) -> bool:
    """
    Check if type or object is a record based on the presence of 'get_key' attribute
    without requiring inheritance from RecordMixin.
    """
    return hasattr(type_or_obj, "get_key")


def is_key(type_or_obj: Any) -> bool:
    """
    Check if type or object is a key (but not a record derived from key) based on the presence of 'get_generic_key'
    attribute and the absence of 'get_key' attribute, without requiring inheritance from KeyMixin.
    """
    return hasattr(type_or_obj, "get_generic_key") and not hasattr(type_or_obj, "get_key")


def is_record_list(type_or_obj: Any) -> bool:
    """
    Check if type or object is a record list based on the presence of 'get_key_list' attribute
    without requiring inheritance from RecordListMixin.
    """
    return hasattr(type_or_obj, "get_key_list")


def is_key_list(type_or_obj: Any) -> bool:
    """
    Check if type or object is a key list based on the presence of 'get_generic_key_list' attribute
    and the absence of 'get_key_list' attribute, without requiring inheritance from KeyListMixin.
    """
    return hasattr(type_or_obj, "get_generic_key_list") and not hasattr(type_or_obj, "get_key_list")


class KeyProtocol(Protocol):
    """Provides primary key fields."""

    def get_generic_key(self) -> Tuple:
        """Tuple of key type followed by the primary key fields (flattened for composite keys)."""


class KeyListProtocol(Protocol):
    """Provides effective compression for a list of keys."""

    def get_generic_key_list(self) -> Tuple:
        """Tuple of key type followed by lists of the primary key fields (flattened for composite keys)."""


class RecordProtocol(KeyProtocol):
    """Provides primary key fields."""

    def get_key(self) -> KeyProtocol:
        """Return key object."""


class RecordListProtocol(KeyListProtocol):
    """Provides effective compression for a list of polymorphic records."""

    def get_key_list(self) -> KeyListProtocol:
        """Return key object."""
