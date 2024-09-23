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
from typing import List

from cl.runtime.plots.group_bar_plot_style_key import GroupBarPlotStyleKey
from cl.runtime.records.record_mixin import RecordMixin


@dataclass(slots=True, kw_only=True)
class GroupBarPlotStyle(GroupBarPlotStyleKey, RecordMixin[GroupBarPlotStyleKey], ABC):
    """Color and layout options for GroupBarPlot."""

    y_ticks: List[float] | None = None
    """Custom y-axis ticks."""

    def get_key(self) -> GroupBarPlotStyleKey:
        return GroupBarPlotStyleKey(style_id=self.style_id)
