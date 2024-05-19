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

from abc import ABC
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.storage.data_source_types import TPackedRecord
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing_extensions import Self

T = TypeVar("T")


@dataclass(slots=True)
class DataclassMixin(RecordMixin, ABC):
    """Mixin methods for dataclass records."""

    def pack(self) -> TPackedRecord:

        # Get data dictionary and remove keys that have None values
        data_dict = asdict(self)
        data_dict = {k: v for k, v in data_dict.items() if v is not None}

        # Return a tuple of key and data
        return self.get_key(), data_dict  # noqa Suppress type warning inside tuple


def datafield(
    *,
    default: T | None = None,
    default_factory: Any | None = None,
    optional: bool = False,
    optional_fields: bool = True,
    subtype: str | None = None,
    name: str | None = None,
    label: str | None = None,
    formatter: str | None = None,
    category: str | None = None,
    secure: bool = False,
    filterable: bool = False,
) -> T:
    """Field in dataclass with additional parameters to define runtime-specific metadata.

    Args:
        default: Default value (None if not specified)
        default_factory: Factory to generate a new instance for default value (for container types)
        optional: If not specified, the field must be set before saving the record.
        optional_fields: Whether the elements of list are optional.
        subtype: Subtype of the field type. Permitted values are `long` for int fields,
        `date` and `datetime` for string fields. TODO(dataclasses) - Review the list, determine which strings to convert
        name: Name of the field in DB, use when standard name conversion is inapplicable due to Python constraints.
        label: Readable name when not obtained by the standard conversion rules.
        formatter: Standard formatter name (without curly brackets) or raw Python format string (in curly brackets)
        category: A group of fields displayed together in the UI. Has no effect outside UI.
        secure: Marks the field as secure TODO(dataclasses) - Explain further in docs
        filterable: Marks the field as filterable TODO(dataclasses) - Explain further in docs
    """
    metadata = {
        "datafield": True,
        "optional": optional,
        "optional_fields": optional_fields,  # TODO(dataclasses) - rename
        "type": subtype,
        "name": name,
        "label": label,
        "format": formatter,  # TODO(dataclasses) - switch to formatter in other places as format causes Python warning
        "category": category,
        "secure": secure,
        "filterable": filterable,
    }
    if default_factory is None:
        return field(default=default, metadata=metadata)
    elif default is None:
        return field(default_factory=default_factory, metadata=metadata)
    else:
        raise RuntimeError(
            f"Params default={default} and default_factory={default_factory} in `datafield` method "
            f"are mutually exclusive but both are specified."
        )
