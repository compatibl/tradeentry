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
from logging import getLogger
from typing import List
from typing import Optional
from typing_extensions import Self
from cl.runtime.records.record_mixin import RecordMixin
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassRecordKey
from stubs.cl.runtime.decorators.stub_viewers_key import StubViewersKey

_logger = getLogger(__name__)


@dataclass(slots=True, kw_only=True)
class StubViewers(StubViewersKey, RecordMixin[StubViewersKey]):
    """Stub record base class."""

    def get_key(self) -> StubViewersKey:
        return StubViewersKey(stub_id=self.stub_id)

    def view_instance_1a(self):
        """Stub viewer with UI element."""
        return {
            "_t": "Script",
            "Name": None,
            "Language": "Markdown",
            "Body": ["# Viewer with UI element", "### _Script_"],
            "WordWrap": None,
        }

    def view_instance_1b(self) -> Optional[str]:
        """Stub viewer with an empty data."""
        return None

    def view_instance_1c(self) -> StubViewersKey:
        """Stub viewer with key data."""
        return self.get_key()

    def view_instance_1d(self) -> Self:
        """Stub viewer with record data."""
        return self

    def view_instance_2a(self) -> List[StubDataclassRecordKey]:
        """Stub viewer with list of keys."""
        return [
            StubDataclassRecordKey(id="Key 1"),
            StubDataclassRecordKey(id="Key 2"),
            StubDataclassRecordKey(id="Key 3"),
        ]

    def view_instance_2b(self) -> List[StubDataclassDerivedRecord]:
        """Stub viewer with list of records."""
        return [
            StubDataclassDerivedRecord(id="Record 1"),
            StubDataclassDerivedRecord(id="Record 2"),
            StubDataclassDerivedRecord(id="Record 3"),
        ]

    def view_instance_2c(self) -> List[Self]:
        """Stub viewer with list of current type's records."""
        return [StubViewers(stub_id="Record 1"), StubViewers(stub_id="Record 2"), StubViewers(stub_id="Record 3")]

    def view_instance_3a(self, param1: str = "Test", param2: str = None):
        """Stub viewer with optional parameters."""

        return {
            "_t": "Script",
            "Name": None,
            "Language": "Markdown",
            "Body": [f"# Viewer with optional parameters", f"### Param1: {param1}", f"### Param2: {param2}"],
            "WordWrap": None,
        }

    # TODO (Ina): introduce more viewer cases
