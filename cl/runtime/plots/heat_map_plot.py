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
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from cl.runtime import Context
from cl.runtime.plots.heat_map_plot_style import HeatMapPlotStyle
from cl.runtime.plots.matplotlib_plot import MatplotlibPlot
from cl.runtime.plots.matplotlib_util import MatplotlibUtil
from cl.runtime.plots.plot import Plot
from cl.runtime.records.dataclasses_extensions import field


@dataclass(slots=True, kw_only=True)
class HeatMapPlot(MatplotlibPlot):
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

    def _create_figure(self) -> plt.Figure:
        # Load style object or create with default settings if not specified
        style = self._load_style()
        theme = self._get_pyplot_theme(style=style)

        received_df, expected_df = (
            pd.DataFrame.from_records(
                [values, self.col_labels, self.row_labels],
                index=['Value', 'Col', 'Row']
            ).T.pivot_table(index="Row", columns="Col", values="Value", sort=False).astype(float)
            for values in [self.received_values, self.expected_values]
        )

        data = (received_df - expected_df).abs()

        with plt.style.context(theme):
            fig, axes = plt.subplots()

            cmap = LinearSegmentedColormap.from_list("rg", ["g", "y", "r"], N=256)

            im = MatplotlibUtil.heatmap(
                data.values, data.index.tolist(), data.columns.tolist(), ax=axes, cmap=cmap
            )

            # Set figure and axes labels
            axes.set_xlabel(self.x_label)
            axes.set_ylabel(self.y_label)
            axes.set_title(self.title)

            fig.tight_layout()

        return fig

    def _load_style(self) -> HeatMapPlotStyle:
        """Load style object or create with default settings if not specified."""
        style = Context.current().load_one(HeatMapPlotStyle, self.style)
        style = style if self.style is not None else HeatMapPlotStyle()

        return style
