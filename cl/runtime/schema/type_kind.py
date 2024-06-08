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


class TypeKind(IntEnum):
    """Type kind enumeration."""

    Final = 0
    """Final type. No types can inherit from final type."""

    Abstract = 1
    """Abstract type. Abstract type can only be saved in storage as parent of another type."""

    Element = 2
    """Element type. Element type cannot be saved in storage directly or as parent of other type."""

    AbstractElement = 3
    """Abstract element type. Abstract element type cannot be saved in storage directly or as parent of other type."""
