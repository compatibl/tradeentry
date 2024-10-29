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
from typing import List
from typing_extensions import Self
from stubs.cl.runtime.views.stub_viewers import StubViewers
from stubs.cl.runtime.views.stub_viewers_key import StubViewersKey


@dataclass(slots=True, kw_only=True)
class StubDataViewers(StubViewers):
    """Stub viewers for data."""

    def view_self(self) -> Self:
        """This viewer will open by default instead of the editor."""
        return self

    def view_none(self) -> str | None:
        """Viewer with optional return type returning None."""
        return None

    def view_key(self) -> StubViewersKey:
        """Viewer returning a key."""
        return self.get_key()

    def view_record(self) -> Self:
        """Viewer returning a record."""
        return self

    def view_key_list(self) -> List[StubViewersKey]:
        """Stub viewer returning a list of keys."""
        return 3 * [self.get_key()]

    def view_record_list(self) -> List[Self]:
        """Stub viewer returning a list of records."""
        return 3 * [self]

    def _view_string(self) -> str:  # TODO: Not yet supported, currenly must wrap into Script content
        """Viewer returning a string."""
        return """A sample multiline string returned by a viewer.
Line 1
Line 2
Line 3
"""

    def _view_with_params(self, param1: str = "Test", param2: str = None):  # TODO: Not supported in this release
        """Stub viewer with optional parameters."""
        return {
            "_t": "Script",
            "Name": None,
            "Language": "Markdown",
            "Body": [f"# Viewer with optional parameters", f"### Param1: {param1}", f"### Param2: {param2}"],
            "WordWrap": None,
        }
