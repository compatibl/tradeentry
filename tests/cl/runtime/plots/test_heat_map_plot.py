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

import pytest
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.plots.heat_map_plot import HeatMapPlot
from cl.runtime.plots.heat_map_plot_style import HeatMapPlotStyle
from cl.runtime.testing.pytest.pytest_fixtures import local_dir_fixture

expected_values = [
    85.5,
    92,
    70,
    83.7,  # "Metric 1"
    89,
    95.3,
    77,
    95,  # "Metric 2"
    81,
    93.6,
    75,
    63.5,  # "Metric 3"
    85.5,
    98.8,
    78,
    83.7,  # "Metric 4"
    79.5,
    90,
    72.4,
    81.8,  # "Metric 5"
]

received_values = [
    85.5,
    94.5,
    70.5,
    85.2,  # "Metric 1"
    77,
    95.3,
    80.4,
    75,  # "Metric 2"
    60,
    98,
    75,
    78.5,  # "Metric 3"
    86,
    95,
    75,
    60,  # "Metric 4"
    77.3,
    92,
    76,
    74,  # "Metric 5"
]

num_metrics = 5
num_models = 4


def test_smoke(local_dir_fixture):
    with TestingContext() as context:
        row_labels = []

        for i in range(num_metrics):
            row_labels += [f"Metric {i + 1}"] * num_models

        col_labels = [f"Model {i + 1}" for i in range(num_models)] * num_metrics

        heat_map_plot = HeatMapPlot(plot_id="heat_map_plot")
        heat_map_plot.title = "Model Comparison"
        heat_map_plot.row_labels = row_labels
        heat_map_plot.col_labels = col_labels
        heat_map_plot.received_values = received_values
        heat_map_plot.expected_values = expected_values
        heat_map_plot.x_label = "Models"
        heat_map_plot.y_label = "Metrics"
        heat_map_plot.save_png()


def test_smoke_dark_theme(local_dir_fixture):
    with TestingContext() as context:
        heat_map_plot_style = HeatMapPlotStyle()
        heat_map_plot_style.dark_theme = True

        row_labels = []

        for i in range(num_metrics):
            row_labels += [f"Metric {i + 1}"] * num_models

        col_labels = [f"Model {i + 1}" for i in range(num_models)] * num_metrics

        heat_map_plot = HeatMapPlot(plot_id="heat_map_plot")
        heat_map_plot.title = "Model Comparison"
        heat_map_plot.row_labels = row_labels
        heat_map_plot.col_labels = col_labels
        heat_map_plot.received_values = received_values
        heat_map_plot.expected_values = expected_values
        heat_map_plot.x_label = "Models"
        heat_map_plot.y_label = "Metrics"
        heat_map_plot.style = heat_map_plot_style
        heat_map_plot.save_png()


if __name__ == "__main__":
    pytest.main([__file__])
