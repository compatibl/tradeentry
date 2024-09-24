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
from cl.runtime.plots.group_bar_plot import GroupBarPlot
from cl.runtime.plots.group_bar_plot_style import GroupBarPlotStyle
from cl.runtime.testing.pytest.pytest_fixtures import local_dir_fixture


def test_smoke(local_dir_fixture):
    with TestingContext() as context:
        bar_plot_style = GroupBarPlotStyle()
        bar_plot_style.y_ticks = list(range(0, 101, 10))

        bar_plot = GroupBarPlot()
        bar_plot.group_labels = ["Group 1", "Group 1"]  # TODO: , "Group 2", "Group 2"]
        bar_plot.bar_labels = ["Bar 11", "Bar 12"]  # TODO: , "Bar 21", "Bar 22"]
        bar_plot.values = [85.5, 92, 70, 83.7]
        bar_plot.style = bar_plot_style

        fig = bar_plot.create_figure()
        fig.savefig("test_bar_plot.test_smoke.png")


if __name__ == "__main__":
    pytest.main([__file__])
