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
from dataclasses import dataclass
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.views.view_key import ViewKey


@dataclass(slots=True, kw_only=True)
class View(ViewKey, RecordMixin, ABC):
    """This type is returned from a viewer method as object or key."""

    def get_key(self) -> ViewKey:
        """Return primary key of this instance in semicolon-delimited string format."""
        return ViewKey(view_for=self.view_for, view_name=self.view_name)
