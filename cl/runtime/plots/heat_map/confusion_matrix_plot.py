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
from typing import List, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.express.colors import sequential as colorscale

from cl.runtime.plots.plot import Plot
from cl.runtime.records.dataclasses_extensions import missing

WHITE_TO_RED_COLORSCALE = ['rgb(255,255,255)'] + colorscale.Reds

YELLOW_TO_WHITE = [
    'rgb(255, 255, 0)',  # Yellow
    'rgb(255, 255, 51)',  # Light Yellow
    'rgb(255, 255, 81)',  # Light Lemon Yellow
    'rgb(255, 255, 102)',  # Pale Yellow
    'rgb(255, 255, 153)',  # Lemon Yellow
    'rgb(255, 255, 204)',  # Soft Yellow
    'rgb(255, 255, 224)',  # Creamy Yellow
    'rgb(255, 255, 240)',  # Very Light
    'rgb(255,255,255)',  # White
]

_layout_background = {
    'paper_bgcolor': 'rgba(255,255,255,1)',
    'plot_bgcolor': 'rgba(255,255,255,1)',
}


@dataclass(slots=True, kw_only=True)
class ConfusionMatrixPlot(Plot):
    """Confusion matrix visualization for a categorical experiment."""

    actual: List[str] = missing()
    """List of actual categories."""

    predicted: List[str] = missing()
    """List of predicted categories in the same order as actual categories."""

    @classmethod
    def create_figure(
            cls,
            data: pd.DataFrame,
            annotation_text: Optional[List[List[str]]] = None,
            matrix_colorscale: Optional[List[str]] = WHITE_TO_RED_COLORSCALE,
            text_color_threshold: Optional[float] = 0.5,
            x_text: Optional[str] = 'Predicted',
            y_text: Optional[str] = 'Real value'
    ) -> go.Figure:
        # Create heatmap
        heatmap = go.Heatmap(
            z=data,
            x=data.index.tolist(),
            y=data.columns.tolist(),
            colorscale=matrix_colorscale,  # Set the colorscale
            showscale=False,  # Hide the colorbar
            hoverinfo='skip'  # Hide hover text
        )

        # Combine both heatmaps into one figure
        fig = go.Figure(data=[heatmap])

        if annotation_text is not None:
            normalized_data = (data / np.nanmax(data)).values

            # Create annotations for each element
            annotations = [
                go.layout.Annotation(
                    text=f'<b>{annotation_text[i][j]}</b>' if i == j else annotation_text[i][j],
                    x=j,
                    y=i,
                    showarrow=False,
                    font=dict(
                        color="black" if normalized_data[i, j] <= text_color_threshold else "white"
                    )
                ) for j in range(data.shape[1]) for i in range(data.shape[0])
            ]

            fig.update_layout(annotations=annotations)

        # Move x-axis to the top
        fig.update_layout(xaxis=dict(side='top'))

        # Set white background
        fig.update_layout(_layout_background)

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

    @staticmethod
    def plot_confusion_matrix(
            data: pd.DataFrame,
            annotation_text: Optional[List[List[str]]] = None,
            diag_colorscale: Optional[List[str]] = colorscale.Greens,
            non_diag_colorscale: Optional[List[str]] = WHITE_TO_RED_COLORSCALE,
            x_text: Optional[str] = 'Predicted',
            y_text: Optional[str] = 'Real value',
            diag_text_color_threshold: Optional[float] = 0.5,
            non_diag_text_color_threshold: Optional[float] = 0.5
    ) -> go.Figure:
        # Create two masks: one for the diagonal and one for the non-diagonal elements
        diag_mask = np.eye(data.shape[0], dtype=bool)
        non_diag_mask = ~diag_mask

        # Create separate data for diagonal and non-diagonal elements
        diag_data = np.where(diag_mask, data, np.nan)  # Diagonal data
        non_diag_data = np.where(non_diag_mask, data, np.nan)  # Non-diagonal data

        # Create heatmap for diagonal elements with a specific colorscale
        diag_heatmap = go.Heatmap(
            z=diag_data,
            x=data.index.tolist(),
            y=data.columns.tolist(),
            colorscale=diag_colorscale,  # Set the colorscale for diagonal
            showscale=False,  # Hide the colorbar for the diagonal
            hoverinfo='skip'  # Hide hover text
        )

        # Create heatmap for non-diagonal elements with another colorscale
        non_diag_heatmap = go.Heatmap(
            z=non_diag_data,
            x=data.index.tolist(),
            y=data.columns.tolist(),
            colorscale=non_diag_colorscale,  # Set the colorscale for non-diagonal
            showscale=False,  # Hide the colorbar for the diagonal
            hoverinfo='skip'  # Hide hover text
        )

        # Combine both heatmaps into one figure
        fig = go.Figure(data=[diag_heatmap, non_diag_heatmap])

        if annotation_text is not None:
            normalized_data = np.nan_to_num(diag_data / np.nanmax(diag_data), nan=0) + \
                              np.nan_to_num(non_diag_data / np.nanmax(non_diag_data), nan=0)

            # Create annotations for each element
            annotations = [
                go.layout.Annotation(
                    text=f'<b>{annotation_text[i][j]}</b>' if i == j else annotation_text[i][j],
                    x=j,
                    y=i,
                    showarrow=False,
                    font=dict(
                        color="black" if normalized_data[i, j] <= (
                            diag_text_color_threshold if i == j else non_diag_text_color_threshold
                        )
                        else "white"
                    )
                ) for j in range(data.shape[1]) for i in range(data.shape[0])
            ]

            fig.update_layout(annotations=annotations)

        # Move x-axis to the top
        fig.update_layout(xaxis=dict(side='top'))

        # Set white background
        fig.update_layout(_layout_background)

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
