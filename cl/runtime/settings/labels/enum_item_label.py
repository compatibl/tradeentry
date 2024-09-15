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
from cl.runtime.settings.labels.enum_item_label_key import EnumItemLabelKey


@dataclass(slots=True, kw_only=True)
class EnumItemLabel(EnumItemLabelKey, RecordMixin[EnumItemLabelKey]):
    """
    Custom enum item label overrides the standard 'ITEM_NAME' -> 'Item Name' transformation.

    Notes:
        - The setting will apply to this item name in every enum
        - This UI setting does not affect the REST API
    """

    enum_item_label: str = missing()
    """Custom enum item label overrides the standard 'ITEM_NAME' -> 'Item Name' transformation."""

    def get_key(self) -> EnumItemLabelKey:
        return EnumItemLabelKey(enum_item_name=self.enum_item_name)
