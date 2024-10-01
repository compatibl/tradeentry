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
from pathlib import Path
import pandas as pd
from cl.runtime import Context
from cl.runtime import RecordMixin
from cl.runtime import viewer
from cl.runtime.backend.core.ui_app_state import UiAppState
from cl.runtime.plots.confusion_matrix_plot import ConfusionMatrixPlot
from cl.runtime.plots.confusion_matrix_plot_style import ConfusionMatrixPlotStyle
from cl.runtime.records.record_mixin import TKey
from cl.runtime.views.plot_view import PlotView
from stubs.cl.runtime.views.stub_plots_key import StubPlotsKey


@dataclass(slots=True, kw_only=True)
class StubPlots(StubPlotsKey, RecordMixin[StubPlotsKey]):
    """Class with plot viewers."""

    def get_key(self) -> TKey:
        return StubPlotsKey(stub_id=self.stub_id)

    @classmethod
    def _create_confusion_matrix_plot(cls):
        """Create confusion matrix plot from data in csv."""
        raw_data = pd.read_csv(Path(__file__).resolve().parent / "./confusion_matrix_plot.csv")

        matrix_plot_style = ConfusionMatrixPlotStyle()
        matrix_plot_style.dark_theme = UiAppState.get_current_user_app_theme() == "Dark"

        matrix_plot = ConfusionMatrixPlot()
        matrix_plot.title = "Confusion Matrix"
        matrix_plot.expected_categories = raw_data["True Category"].values.tolist()
        matrix_plot.received_categories = raw_data["Predicted"].values.tolist()
        matrix_plot.style = matrix_plot_style

        return matrix_plot

    @viewer
    def confusion_matrix_plot_png_view(self):
        """Png viewer for MatplotlibPlot with theme."""

        # Create ConfusionMatrixPlot instance
        matrix_plot = self._create_confusion_matrix_plot()

        # Return PngView
        return matrix_plot.get_view()

    @viewer
    def confusion_matrix_plot_view_with_record(self):
        """Plot viewer for MatplotlibPlot as record with theme."""

        # Create ConfusionMatrixPlot instance
        matrix_plot = self._create_confusion_matrix_plot()

        # Return PlotView
        return PlotView(plot=matrix_plot)

    @viewer
    def confusion_matrix_plot_view_with_key(self):
        """Plot viewer for MatplotlibPlot as key with theme."""

        # Create ConfusionMatrixPlot instance
        matrix_plot = self._create_confusion_matrix_plot()
        matrix_plot.plot_id = "confusion_matrix_plot"

        Context.current().save_one(matrix_plot)

        # Return PlotView
        return PlotView(plot=matrix_plot.get_key())
