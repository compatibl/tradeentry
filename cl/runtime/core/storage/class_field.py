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

from dataclasses import field
from typing import Any, Optional


def class_field(
    *,
    optional: bool = False,
    typename: Optional[str] = None,  # TODO: Rename typename to subtype
    name: Optional[str] = None,
    label: Optional[str] = None,
) -> Any:
    """Field in dataclass with additional parameters to define runtime-specific metadata.

    Args:
        optional: If not specified, the field must be set before saving the record.
        typename: Subtype of the main type. Permitted values are `long` for int fields,
        `date` and `datetime` for string fields. TODO - Provide a complete list
        name: TODO - Clarify the purpose in comment
        label: Readable name when not obtained by the standard conversion rules.
    """
    return field(
        default=None,
        metadata={
            'class_field': True,
            'optional': optional,
            'typename': typename,
            'name': name,
            'label': label},
        )
