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
import pandas as pd
from cl.runtime.plots.bar.bar_plot import BarPlot
from cl.runtime.testing.pytest.pytest_fixtures import local_dir_fixture


def test_smoke(local_dir_fixture):
    data = pd.Series({"Model 1": 85.5, "Model 2": 92, "Model 3": 70, "Model 4": 83.7})

    fig = BarPlot.create_figure(data=data, ticks=np.arange(0, 101, 10))
    fig.write_image("test_bar_plot.test_smoke.png")


if __name__ == "__main__":
    pytest.main([__file__])
