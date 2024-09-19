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
from typing import Optional, List
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from cl.runtime.plots.bar.bar_plot_style import BarPlotStyle
from cl.runtime.plots.bar.bar_plot_style_key import BarPlotStyleKey
from cl.runtime.plots.plot import Plot
from cl.runtime.records.dataclasses_extensions import missing, field

_layout_background = {
    'paper_bgcolor': 'rgba(255,255,255,1)',
    'plot_bgcolor': 'rgba(255,255,255,1)',
}


@dataclass(slots=True, kw_only=True)
class BarPlot(Plot):
    
    labels: List[str] = missing()
    """List of bar labels."""
    
    values: List[str] = missing()
    """List of bar values in the same order as labels."""

    style: BarPlotStyleKey = field(default_factory=lambda: BarPlotStyle())
    """Color and layout options."""

    @classmethod
    def create_figure(
            cls,
            data: pd.Series,
            ticks: Optional[np.ndarray] = None,
            x_text: Optional[str] = 'Experiment',
            y_text: Optional[str] = 'Value'
    ) -> go.Figure:
        bars = go.Bar(
            x=data.index,
            y=data
        )

        # Combine both heatmaps into one figure
        fig = go.Figure(data=bars)

        # Set white background
        fig.update_layout(_layout_background)

        # Custom ticks if provided
        if ticks is not None:
            y_min = np.nanmin(ticks)
            y_max = np.nanmax(ticks)

            for value in [y_min, y_max]:
                fig.add_hline(y=value, opacity=0, showlegend=False)

            fig.update_layout(yaxis=dict(tickvals=ticks))

        # add custom xaxis title
        fig.add_annotation(dict(font=dict(color="black", size=14),
                                x=0.5,
                                y=-0.15,
                                showarrow=False,
                                text=x_text,
                                xref="paper",
                                yref="paper"))

        # add custom yaxis title
        fig.add_annotation(dict(font=dict(color="black", size=14),
                                x=-0.35,
                                y=0.5,
                                showarrow=False,
                                text=y_text,
                                textangle=-90,
                                xref="paper",
                                yref="paper"))

        return fig
