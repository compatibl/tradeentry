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
from matplotlib.colors import LinearSegmentedColormap

from cl.runtime import Context
from cl.runtime.plots.heat_map_plot_style import HeatMapPlotStyle
from cl.runtime.plots.heat_map_plot_style_key import HeatMapPlotStyleKey
from cl.runtime.plots.matplotlib_util import MatplotlibUtil
from cl.runtime.plots.plot import Plot
from cl.runtime.records.dataclasses_extensions import field


@dataclass(slots=True, kw_only=True)
class HeatMapPlot(Plot):
    """Heat map visualization."""

    title: str = field()
    """Plot title."""

    row_labels: List[str] = field()
    """Row label for each cell in the same order of cells as other fields."""

    col_labels: List[str] = field()
    """Column label for each cell in the same order of cells as other fields."""

    received_values: List[str] = field()
    """Received value for each cell in the same order of cells as other fields."""

    expected_values: List[str] = field()
    """Expected (correct) value for each cell in the same order of cells as other fields."""

    x_label: str = field()
    """x-axis label."""

    y_label: str = field()
    """y-axis label."""

    style: HeatMapPlotStyleKey = field(default_factory=lambda: HeatMapPlotStyle())
    """Color and layout options."""

    def create_figure(self) -> plt.Figure:

        # Load style object
        style = Context.current().load_one(HeatMapPlotStyle, self.style)

        theme = 'dark_background' if style.dark_theme else 'default'

        with plt.style.context(theme):
            fig, axes = plt.subplots()

            shape = (len(self.row_labels), len(self.col_labels))

            data = np.abs(
                np.reshape(np.asarray(self.received_values), shape) - np.reshape(np.asarray(self.expected_values),
                                                                                 shape)
            )

            cmap = LinearSegmentedColormap.from_list('rg', ["g", "y", "r"], N=256)

            im = MatplotlibUtil.heatmap(data, self.row_labels, self.col_labels, ax=axes, cmap=cmap)

            # Set figure and axes labels
            axes.set_xlabel(self.x_label)
            axes.set_ylabel(self.y_label)
            axes.set_title(self.title)

            fig.tight_layout()

        return fig
