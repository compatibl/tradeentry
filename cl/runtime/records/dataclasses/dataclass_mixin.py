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
from typing import Any, Callable
from typing import TypeVar

TDefault = TypeVar("TDefault")
TDefaultFactory = Callable[[], TDefault]


@dataclass(slots=True, kw_only=True)
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
    default: TDefault | None = None,
    default_factory: TDefaultFactory | None = None,
    name: str | None = None,  # TODO: Review use when trailing _ is removed automatically
    label: str | None = None,
    subtype: str | None = None,
    formatter: str | None = None,
) -> TDefault:
    """Field in dataclass with additional parameters to define runtime-specific metadata.

    Args:
        default: Default value (None if not specified)
        default_factory: Factory to generate a new instance for default value (for container types)
        name: Override field name in REST (label will be titleized version of this parameter)
        label: Override titleized name in UI
        subtype: Override field type, the only permitted value is `long` for int field type
        formatter: Standard formatter name (without curly brackets) or raw Python format string (in curly brackets)
    """
    metadata = {
        "name": name,
        "label": label,
        "subtype": subtype,
        "formatter": formatter,  # TODO: switch to formatter in other places as format causes Python warnings
    }
    if default_factory is None:
        return field(default=default, metadata=metadata)
    elif default is None:
        return field(default_factory=default_factory, metadata=metadata)
    else:
        raise RuntimeError(
            f"Params default={default} and default_factory={default_factory} "
            f"are mutually exclusive but both are specified."
        )
