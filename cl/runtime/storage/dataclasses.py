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

from typing import Any, Optional
from typing_extensions import dataclass_transform

from cl.runtime.storage.attrs import attrs_field, attrs_class, attrs_class_impl


def data_field(
    *,
    default: Optional[Any] = None,
    factory: Optional[Any] = None,
    optional: bool = False,
    optional_fields: bool = True,
    subtype: Optional[str] = None,
    name: Optional[str] = None,
    label: Optional[str] = None,
    formatter: Optional[str] = None,
    category: Optional[str] = None,
    secure: bool = False,
    filterable: bool = False,
) -> Any:
    """Field in dataclass with additional parameters to define runtime-specific metadata.

    Args:
        default: Default value (None if not specified)
        factory: Factory to generate a new instance for default value (for container types)
        optional: If not specified, the field must be set before saving the record.
        optional_fields: Whether the elements of list are optional.
        subtype: Subtype of the field type. Permitted values are `long` for int fields,
        `date` and `datetime` for string fields. TODO(attrs) - Review the list, determine which strings to convert
        name: Name of the field in DB, use when standard name conversion is inapplicable due to Python constraints.
        label: Readable name when not obtained by the standard conversion rules.
        formatter: Standard formatter name (without curly brackets) or raw Python format string (in curly brackets)
        category: A group of fields displayed together in the UI. Has no effect outside UI.
        secure: Marks the field as secure TODO(attrs) - Explain further in docs
        filterable: Marks the field as filterable TODO(attrs) - Explain further in docs
    """
    return attrs_field(
        default=default,
        factory=factory,
        optional=optional,
        optional_fields=optional_fields,
        subtype=subtype,
        name=name,
        label=label,
        formatter=formatter,
        category=category,
        secure=secure,
        filterable=filterable
        )


@dataclass_transform()
def data_class_impl(cls, *, init: bool = True, label: str = None):
    """Performs the actual wrapping irrespective of call syntax with or without parentheses."""
    return attrs_class_impl(cls=cls, init=init, label=label)


@dataclass_transform()
def data_class(cls=None, *, init: bool = True, label: str = None):
    """Runtime decorator dataclasses."""
    return attrs_class(cls=cls, init=init, label=label)
