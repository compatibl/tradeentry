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
from cl.runtime.storage.enum_util import enum_class


@enum_class(label="Stub Int Enum New Label")
class StubRelabeledIntEnum(IntEnum):
    """Stub enum with custom label that does not match the name."""

    ENUM_VALUE_1 = 1
    """Enum value 1."""

    ENUM_VALUE_2 = 2
    """Enum value 2."""
