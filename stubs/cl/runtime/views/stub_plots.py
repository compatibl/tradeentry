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

from cl.runtime import RecordMixin
from cl.runtime.records.record_mixin import TKey
from stubs.cl.runtime.decorators.stub_handlers_key import StubHandlersKey
from stubs.cl.runtime.views.stub_plots_key import StubPlotsKey


@dataclass(slots=True, kw_only=True)
class StubPlots(StubPlotsKey, RecordMixin[StubPlotsKey]):
    """Class with plot viewers."""

    def get_key(self) -> TKey:
        return StubHandlersKey(stub_id=self.stub_id)