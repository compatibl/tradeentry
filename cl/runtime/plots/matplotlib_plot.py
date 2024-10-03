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
from abc import abstractmethod
from dataclasses import dataclass
from cl.runtime.plots.plot import Plot
from matplotlib import pyplot as plt
from cl.runtime.testing.stack_util import StackUtil


@dataclass(slots=True, kw_only=True)
class MatplotlibPlot(Plot):
    """Base class for plot objects created using Matplotlib package."""

    @abstractmethod
    def _create_figure(self) -> plt.Figure:
        """Return Matplotlib figure object for the plot."""

    def save_png(self) -> None:
        """Implement using 'create_figure' method."""

        # Create figure
        fig = self._create_figure()

        # Create directory if does not exist
        base_dir = StackUtil.get_base_dir()
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # Check that plot_id is set
        if self.plot_id is None or self.plot_id == "":
            raise RuntimeError("Cannot save figure as png because 'plot_id' field is not set.")

        # Save
        file_path = os.path.join(base_dir, f"{self.plot_id}.png")
        fig.savefig(file_path)
