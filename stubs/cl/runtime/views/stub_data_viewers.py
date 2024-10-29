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

from stubs.cl.runtime import StubDataclassRecordKey, StubDataclassRecord, StubDataclassNestedFields, \
    StubDataclassListFields, StubDataclassComposite, StubDataclassCompositeKey
from stubs.cl.runtime.views.stub_viewers import StubViewers
from stubs.cl.runtime.views.stub_viewers_key import StubViewersKey

nested_fields_key = StubDataclassRecordKey(id="nested_1")
"""Key returned by the viewer."""

nested_fields_record = StubDataclassNestedFields()
"""Record returned by the viewer."""

list_fields_record = StubDataclassListFields()
"""Record returned by the viewer."""

composite_key = StubDataclassCompositeKey()
"""Record returned by the viewer."""

composite_record = StubDataclassComposite()
"""Record returned by the viewer."""


@dataclass(slots=True, kw_only=True)
class StubDataViewers(StubViewers):
    """Stub viewers for data."""

    def view_self(self) -> Self:
        """This viewer will open by default instead of the editor."""
        return nested_fields_key

    def view_none(self) -> str | None:
        """Viewer with optional return type returning None."""
        return None

    def view_nested_fields_key(self) -> StubDataclassRecordKey:
        """Viewer returning a key."""
        return nested_fields_key

    def view_composite_key(self) -> StubDataclassCompositeKey:
        """Viewer returning a key."""
        return composite_key

    def view_nested_fields_record(self) -> StubDataclassNestedFields:
        """Viewer returning a record."""
        return nested_fields_record

    def view_list_fields_record(self) -> StubDataclassListFields:
        """Viewer returning a record."""
        return list_fields_record

    def view_composite_record(self) -> StubDataclassComposite:
        """Viewer returning a key."""
        return composite_record

    def view_key_list(self) -> List[StubDataclassRecordKey]:
        """Stub viewer returning a list of keys."""
        return 3 * [nested_fields_key]

    def view_record_list(self) -> List[StubDataclassNestedFields]:
        """Stub viewer returning a list of records."""
        return 3 * [nested_fields_record]

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
