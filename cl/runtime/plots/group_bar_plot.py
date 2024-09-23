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

import numpy as np
from matplotlib import pyplot as plt

from cl.runtime import Context
from cl.runtime.plots.group_bar_plot_style import GroupBarPlotStyle
from cl.runtime.plots.group_bar_plot_style_key import GroupBarPlotStyleKey
from cl.runtime.plots.plot import Plot
from cl.runtime.records.dataclasses_extensions import field

_layout_background = {
    "paper_bgcolor": "rgba(255,255,255,1)",
    "plot_bgcolor": "rgba(255,255,255,1)",
}


@dataclass(slots=True, kw_only=True)
class GroupBarPlot(Plot):
    """Base class for the 2D bar plot."""

    title: str = field()
    """Plot title."""

    x_label: str = field(default="Groups")
    """x-axis label."""

    y_label: str = field(default="Value")
    """y-axis label."""

    bar_labels: List[str] = field()
    """List of bar labels."""

    group_labels: List[str] = field()
    """List of group labels."""

    values: List[float] = field()
    """List of values in the same order as bar and group labels."""

    style: GroupBarPlotStyleKey = field(default_factory=lambda: GroupBarPlotStyle())
    """Color and layout options."""

    def create_figure(self) -> plt.Figure:

        # Load style object
        style = Context.current().load_one(GroupBarPlotStyle, self.style)

        fig = plt.figure()
        axes = fig.add_subplot()

        x_ticks = np.arange(len(self.group_labels))

        if len(self.bar_labels) % 2 != 0:
            bar_shifts_positive = list(range(1, len(self.bar_labels) // 2 + 1))
        else:
            bar_shifts_positive = [x / 2 for x in range(1, len(self.bar_labels) // 2 + 1)]

        bar_shifts = [-x for x in reversed(bar_shifts_positive)]

        if len(self.bar_labels) % 2 != 0:
            bar_shifts += [0]

        bar_shifts += bar_shifts_positive

        space = 1 / (len(self.bar_labels) + 1)

        for i, (bar_label, bar_shift) in enumerate(zip(self.bar_labels, bar_shifts)):
            data = self.values[i * len(self.group_labels): (i + 1) * len(self.group_labels)]
            axes.bar(x_ticks + space * bar_shift, data, space, label=bar_label)

        axes.set_xticks(x_ticks, self.group_labels)

        if style.y_ticks is not None:
            axes.set_yticks(style.y_ticks)

        # Set figure and axes labels
        axes.set_xlabel(self.x_label)
        axes.set_ylabel(self.y_label)
        axes.set_title(self.title)

        # Add legend
        axes.legend()

        return fig
