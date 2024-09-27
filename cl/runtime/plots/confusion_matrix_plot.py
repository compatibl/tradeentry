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
import os
from dataclasses import dataclass
from typing import List
from typing import Tuple
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from cl.runtime import Context
from cl.runtime.plots.confusion_matrix_plot_style import ConfusionMatrixPlotStyle
from cl.runtime.plots.confusion_matrix_plot_style_key import ConfusionMatrixPlotStyleKey
from cl.runtime.plots.matplotlib_util import MatplotlibUtil
from cl.runtime.plots.matrix_util import MatrixUtil
from cl.runtime.plots.plot import Plot
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.testing.stack_util import StackUtil


@dataclass(slots=True, kw_only=True)
class ConfusionMatrixPlot(Plot):
    """Confusion matrix visualization for a categorical experiment."""

    title: str = field()
    """Plot title."""

    received_categories: List[str] = field()
    """List of received (predicted) categories for each trial."""

    expected_categories: List[str] = field()
    """List of expected (correct) categories in the same order of trials as received (predicted) categories."""

    x_label: str | None = "Predicted"
    """x-axis label."""

    y_label: str | None = "Correct"
    """y-axis label."""

    style: ConfusionMatrixPlotStyleKey = field(default_factory=lambda: ConfusionMatrixPlotStyle())
    """Color and layout options."""

    def create_figure(self) -> plt.Figure:
        # Load style object
        style = Context.current().load_one(ConfusionMatrixPlotStyle, self.style)

        # TODO: consider moving
        data, annotation_text = self._create_confusion_matrix()

        theme = "dark_background" if style.dark_theme else "default"

        with plt.style.context(theme):
            fig, axes = plt.subplots()

            cmap = LinearSegmentedColormap.from_list("rg", ["g", "y", "r"], N=256)

            im = MatplotlibUtil.heatmap(data.values, data.index.tolist(), data.columns.tolist(), ax=axes, cmap=cmap)
            MatplotlibUtil.annotate_heatmap(im, labels=annotation_text, textcolors="black", size=style.label_font_size)

            # Set figure and axes labels
            axes.set_xlabel(self.x_label)
            axes.set_ylabel(self.y_label)
            axes.set_title(self.title)

            fig.tight_layout()

        return fig

    def _create_confusion_matrix(self) -> Tuple[pd.DataFrame, List[List[str]]]:
        raw_data = pd.DataFrame({"Actual": self.expected_categories, "Predicted": self.received_categories})

        data_confusion_matrix = MatrixUtil.create_confusion_matrix(
            data=raw_data, true_column_name="Actual", predicted_column_name="Predicted"
        )
        data_confusion_matrix_percent = MatrixUtil.convert_confusion_matrix_to_percent(data=data_confusion_matrix)
        diag_mask = np.eye(data_confusion_matrix_percent.shape[0], dtype=bool)
        data_confusion_matrix_error_percent = data_confusion_matrix_percent.copy()
        data_confusion_matrix_error_percent.values[diag_mask] = 100 - np.diag(data_confusion_matrix_percent)
        annotation_text = MatrixUtil.create_confusion_matrix_labels(data=data_confusion_matrix, in_percent=True)

        return data_confusion_matrix_error_percent, annotation_text
