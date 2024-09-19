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
import numpy as np
from cl.runtime.plots.bar.bar_plot import BarPlot
from cl.runtime.testing.pytest.pytest_fixtures import local_dir_fixture


def test_smoke(local_dir_fixture):
    bar_plot = BarPlot()
    bar_plot.labels = ["Model 1", "Model 2", "Model 3", "Model 4"]
    bar_plot.values = [85.5, 92, 70, 83.7]

    fig = bar_plot.create_figure(ticks=np.arange(0, 101, 10))
    fig.write_image("test_bar_plot.test_smoke.png")


if __name__ == "__main__":
    pytest.main([__file__])
