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

from dataclasses import dataclass
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.settings.labels.field_label_key import FieldLabelKey


@dataclass(slots=True, kw_only=True)
class FieldLabel(FieldLabelKey, RecordMixin[FieldLabelKey]):
    """
    Custom field label overrides the standard 'field_name' -> 'Field Name' transformation.

    Notes:
        - The setting will apply to this field name in every class
        - This UI setting does not affect the REST API
    """

    field_label: str = missing()
    """Custom field label overrides the standard 'field_name' -> 'Field Name' transformation."""

    def get_key(self) -> FieldLabelKey:
        return FieldLabelKey(field_name=self.field_name)
