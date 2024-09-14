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

from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.serialization.dict_serializer import _get_class_hierarchy_slots  # TODO: Move to ClassInfo
from cl.runtime.storage.data_source_types import TDataDict
from dataclasses import dataclass
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Type


@dataclass(slots=True, kw_only=True)
class MongoFilterSerializer:
    """Serialize record for use as a MongoDB query filter."""

    primitive_type_names: ClassVar[Type] = ["str", "float", "int", "bool", "date", "time", "datetime", "bytes", "UUID"]
    """
    Detect primitive type by checking if class name is in this list, compare strings rather than types to support 
    detection of custom type definitions that exist in more than one package such as UUID.
    """

    def serialize_filter(self, data: RecordProtocol) -> TDataDict:
        """Serialize record for use as a MongoDB query filter."""

        # Get slots from this class and its bases in the order of declaration from base to derived
        all_slots = _get_class_hierarchy_slots(data.__class__)
        # Serialize slot values in the order of declaration except those that are None
        result = {
            k: v if v.__class__.__name__ in self.primitive_type_names else self._not_primitive_field_error(data, k, v)
            for k in all_slots
            if (v := getattr(data, k)) is not None
        }
        return result

    @classmethod
    def _not_primitive_field_error(cls, data: RecordProtocol, k: str, v: Any) -> None:
        """Error indicating only primitive field names are supported."""
        raise RuntimeError(
            f"Field '{k}' in '{data.__class__.__name__}' has type '{type(v)}'. This field cannot "
            f"be used in a database filter because it is not one of the supported primitive types: "
            + ", ".join(f"'{cls.primitive_type_names}'")
            + "."
        )
