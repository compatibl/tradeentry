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

import plotly.graph_objects as go

from cl.runtime.backend.core.ui_app_state import UiAppState
from cl.runtime.view.binary_content import BinaryContent
from cl.runtime.view.binary_content_type_enum import BinaryContentTypeEnum


class PlotLightTheme:
    """
    Constants for light theme.
    """

    BACKGROUND_COLOR = '#FFFFFF'
    FONT_SIZE = 13
    FONT_COLOR = '#212121'
    FONT_FAMILY = 'Roboto'
    GRID_COLOR = '#DFE8F3'
    ZERO_LINE_COLOR = '#EBF0F8'


class PlotDarkTheme:
    """
    Constants for dark theme.
    """

    BACKGROUND_COLOR = '#212121'
    FONT_SIZE = 13
    FONT_COLOR = '#bdbdbd'
    FONT_FAMILY = 'Roboto'
    GRID_COLOR = '#303030'
    ZERO_LINE_COLOR = '#494949'


def get_plot_template(dark_theme: bool) -> go.layout.Template:
    """Creates plot's theme."""

    color_theme: PlotDarkTheme | PlotLightTheme
    if dark_theme:
        color_theme = PlotDarkTheme()
    else:
        color_theme = PlotLightTheme()
    plot_font = go.layout.Font(size=color_theme.FONT_SIZE, family=color_theme.FONT_FAMILY, color=color_theme.FONT_COLOR)
    plot_axes = dict(gridcolor=color_theme.GRID_COLOR, zerolinecolor=color_theme.ZERO_LINE_COLOR)
    plot_scene_axes = dict(backgroundcolor=color_theme.BACKGROUND_COLOR, **plot_axes)

    plot_layout = go.Layout(
        plot_bgcolor=color_theme.BACKGROUND_COLOR,
        paper_bgcolor=color_theme.BACKGROUND_COLOR,
        font=plot_font,
        title=go.layout.Title(x=0.5),
        xaxis=plot_axes,
        yaxis=plot_axes,
        scene=go.layout.Scene(xaxis=plot_scene_axes, yaxis=plot_scene_axes, zaxis=plot_scene_axes),
    )

    return go.layout.Template(layout=plot_layout)


def get_plot_content(figure: go.Figure, dark_theme: bool = False, use_app_theme: bool = False) -> BinaryContent:
    """Creates binary content for plot."""

    if use_app_theme:
        dark_theme = UiAppState.get_current_user_app_theme() == 'Dark'

    figure.update_layout(template=get_plot_template(dark_theme))
    # Create plot view content
    plot_content = BinaryContent()
    plot_html_str = figure.to_html(include_plotlyjs=False, full_html=False)
    plot_content.content = str.encode(plot_html_str)
    plot_content.content_type = BinaryContentTypeEnum.Plotly
    return plot_content
