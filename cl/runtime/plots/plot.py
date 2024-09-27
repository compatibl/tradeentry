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
from abc import ABC
from dataclasses import dataclass
from cl.runtime.plots.plot_key import PlotKey
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.testing.stack_util import StackUtil


@dataclass(slots=True, kw_only=True)
class Plot(PlotKey, RecordMixin[PlotKey], ABC):
    """Base class for plot objects."""

    def get_key(self) -> PlotKey:
        return PlotKey(plot_id=self.plot_id)

    def save(self, *, ext: str = "png") -> None:
        """Save to 'base_dir/plot_id.ext'."""
        fig = self.create_figure()  # TODO: Must implement abstract method, works because all plots are Matplotlib
        base_dir = StackUtil.get_base_dir()
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        ext = ext[1:] if ext.startswith(".") else ext
        fig.savefig(os.path.join(base_dir, f"{self.plot_id}.{ext}"))
