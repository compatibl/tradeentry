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
import plotly.graph_objects as go
from cl.runtime import Context
from cl.runtime.plots.bar_plot_style import BarPlotStyle
from cl.runtime.plots.bar_plot_style_key import BarPlotStyleKey
from cl.runtime.plots.plot import Plot
from cl.runtime.plots.plotly_util import PlotlyUtil
from cl.runtime.records.dataclasses_extensions import field

_layout_background = {
    "paper_bgcolor": "rgba(255,255,255,1)",
    "plot_bgcolor": "rgba(255,255,255,1)",
}


@dataclass(slots=True, kw_only=True)
class BarPlot(Plot):
    """Base class for the 2D bar plot."""

    labels: List[str] = field()
    """List of bar labels."""

    values: List[float] = field()
    """List of bar values in the same order as labels."""

    style: BarPlotStyleKey = field(default_factory=lambda: BarPlotStyle())
    """Color and layout options."""

    def create_figure(self) -> go.Figure:
        # load style object
        style = Context.current().load_one(BarPlotStyle, self.style)

        bars = go.Bar(x=self.labels, y=self.values)

        # Combine both heatmaps into one figure
        fig = go.Figure(data=bars)

        # Set white background
        fig.update_layout(_layout_background)

        # Custom ticks if provided
        if style.ticks is not None:
            y_min = min(style.ticks)
            y_max = max(style.ticks)

            for value in [y_min, y_max]:
                fig.add_hline(y=value, opacity=0, showlegend=False)

            fig.update_layout(yaxis=dict(tickvals=style.ticks))

        # add custom xaxis title
        fig.add_annotation(
            dict(
                font=dict(color=style.axis_label_font_color, size=style.axis_label_font_size),
                x=0.5,
                y=-0.15,
                showarrow=False,
                text=style.x_label,
                xref="paper",
                yref="paper",
            )
        )

        # add custom yaxis title
        fig.add_annotation(
            dict(
                font=dict(color=style.axis_label_font_color, size=style.axis_label_font_size),
                x=-0.35,
                y=0.5,
                showarrow=False,
                text=style.y_label,
                textangle=-90,
                xref="paper",
                yref="paper",
            )
        )

        # Show if show_limit is not yet reached (configure via settings, default is zero)
        PlotlyUtil.show_if_below_limit(fig)

        return fig
