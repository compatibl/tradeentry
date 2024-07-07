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

from cl.runtime.records.dataclasses_util import datafield
from cl.runtime.records.key_mixin import KeyMixin
from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True, kw_only=True)
class ViewKey(KeyMixin):
    """Contains data that will be visualized alongside the record specified by the 'view_for' field."""

    view_for: Tuple = datafield()
    """Generic key of the record for which the view is specified."""

    view_name: str = datafield()
    """Name of the view displayed in the front end."""

    def get_generic_key(self) -> Tuple:
        return ViewKey, self.view_for, self.view_name
