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

from typing import Any, TypeGuard
from typing import Protocol
from typing import Type


class KeyProtocol(Protocol):
    """Protocol implemented by keys and also required for records which are derived from keys."""

    @classmethod
    def get_key_type(cls) -> Type:
        """Return key type even when called from a record."""


class RecordProtocol(KeyProtocol):
    """Protocol implemented by records but not keys."""

    def get_key(self) -> KeyProtocol:
        """Return a new key object whose fields populated from self, do not return self."""


class InitProtocol:
    """Protocol implemented by objects that require initialization."""

    def init(self) -> None:
        """Similar to __init__ but uses previously set fields instead of parameters."""


class ValidateProtocol:
    """Protocol implemented by objects that support validation."""

    def validate(self) -> None:
        """Confirm that previously set fields correspond to a valid object state."""


def is_record(type_or_obj: Any) -> TypeGuard[RecordProtocol]:
    """Check if type or object is a key (supports RecordProtocol) based on the presence of 'get_key' attribute."""
    return hasattr(type_or_obj, "get_key")


def is_key(type_or_obj: Any) -> TypeGuard[KeyProtocol]:
    """
    Check if type or object is a key (supports KeyProtocol) but not a record (does not support RecordProtocol)
    based on the presence of 'get_key_type' attribute and the absence of 'get_key' attribute.
    """
    return hasattr(type_or_obj, "get_key_type") and not hasattr(type_or_obj, "get_key")


def has_init(type_or_obj: Any) -> TypeGuard[InitProtocol]:
    """Check if type or object requires initialization (InitProtocol) based on the presence of 'init' attribute."""
    return hasattr(type_or_obj, "init")


def has_validate(type_or_obj: Any) -> TypeGuard[ValidateProtocol]:
    """Check if type or object supports validation (ValidateProtocol) based on the presence of 'validate' attribute."""
    return hasattr(type_or_obj, "validate")
