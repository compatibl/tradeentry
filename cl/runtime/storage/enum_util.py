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


def enum_class_impl(cls, *, label=None):
    """Performs the actual wrapping irrespective of call syntax with or without parentheses."""

    if not issubclass(cls, IntEnum):
        raise TypeError("Expected StrEnum or IntEnum derived type.")  # TODO: Review if StrEnum should be used

    # Add label if specified
    if label is not None:
        cls._label = label

    return cls


def enum_class(cls=None, *, label=None):
    """Runtime decorator for key, record, and data classes."""

    # The value of cls type depends on whether parentheses follow the decorator.
    # It is the class when used as @enum_class but None for @enum_class().
    if cls is None:
        return enum_class_impl
    else:
        return enum_class_impl(cls, label=label)
