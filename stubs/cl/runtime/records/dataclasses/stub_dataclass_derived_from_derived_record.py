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

from __future__ import annotations

from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.primitive.date_time_util import DateTimeUtil
from cl.runtime.primitive.date_util import DateUtil
from dataclasses import dataclass
from stubs.cl.runtime.records.dataclasses.stub_dataclass_derived_record import StubDataclassDerivedRecord
from typing import Optional


@dataclass
class StubDataclassDerivedFromDerivedRecord(StubDataclassDerivedRecord):
    """Two levels in inheritance hierarchy away from StubDataclassRecord."""

    derived_from_derived_field: str = datafield(default="derived_from_derived")
    """Stub field."""
