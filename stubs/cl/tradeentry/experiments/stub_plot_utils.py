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

from typing import List

from matplotlib import pyplot as plt

from cl.runtime.plots.group_bar_plot import GroupBarPlot


def create_group_bar_plot(results: List[float], bar_labels: List[str], group_labels: List[str]) -> plt.Figure:
    group_bar_plot = GroupBarPlot()
    group_bar_plot.bar_labels = bar_labels
    group_bar_plot.group_labels = group_labels
    group_bar_plot.value_ticks = list(range(0, 101, 10))
    group_bar_plot.values = results
    return group_bar_plot.create_figure()
