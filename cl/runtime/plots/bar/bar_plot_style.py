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
from typing import List, Any, Dict

from cl.runtime.plots.bar.bar_plot_style_key import BarPlotStyleKey
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.record_mixin import RecordMixin


@dataclass(slots=True, kw_only=True)
class BarPlotStyle(BarPlotStyleKey, RecordMixin[BarPlotStyleKey], ABC):
    """Color and layout options for BarPlot."""

    axis_origin: float = 0.0
    """Origin of axis (defaults to zero if not specified)."""

    axis_min: float = 0.0
    """Lower limit of axis range (defaults to zero if not specified). Data outside the range is permitted."""

    axis_max: float | None = None
    """Upper limit of axis (maximum data value is used when not specified). Data outside the range is permitted."""

    ticks: List[float] | None = None
    """Custom x-axis ticks."""

    x_label: str | None = "Experiment"
    """x-axis label."""

    y_label: str | None = "Value"
    """y-axis label."""

    axis_label_font_size: int = 14
    """Axis labels font size."""

    axis_label_font_color: str = 'black'
    """Axis labels font color."""

    layout_background: Dict[str, Any] = field(default_factory=lambda: {
        "paper_bgcolor": "rgba(255,255,255,1)", "plot_bgcolor": "rgba(255,255,255,1)"
    })

    def get_key(self) -> BarPlotStyleKey:
        return BarPlotStyleKey(style_id=self.style_id)
