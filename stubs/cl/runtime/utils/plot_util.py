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

import plotly.express as px
import plotly.graph_objects as go

from cl.runtime.plots.plotly_util import PlotlyUtil


def create_multi_line_plot() -> go.Figure:
    """Create a multi-line plot."""

    df_data = px.data.stocks()
    fig = go.Figure()

    # Add plots to the same layout
    fig.add_trace(go.Scatter(x=df_data["date"], y=df_data["GOOG"], mode="lines", name="Google"))
    fig.add_trace(go.Scatter(x=df_data["date"], y=df_data["AAPL"], mode="lines", name="Apple"))
    fig.add_trace(go.Scatter(x=df_data["date"], y=df_data["AMZN"], mode="lines", name="Amazon"))
    fig.update_layout(xaxis_tickformat="%d %B (%a)<br>%Y", title="Stocks")

    # Show if show_limit is not yet reached (configure via settings, default is zero)
    PlotlyUtil.show_if_below_limit(fig)

    return fig
