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

import plotly.graph_objects as go
from cl.runtime.settings.plotly_settings import PlotlySettings


class PlotlyUtil:
    """Utilities for plots created using Plotly."""

    _show_counter = 0
    """Count how many times a plot has been shown during the session, used to apply 'show_limit'."""

    @classmethod
    def show_if_below_limit(cls, figure: go.Figure, *args, **kwargs) -> None:
        """Invoke figure.show until show_limit is reached."""

        # Check the show counter
        plotly_settings = PlotlySettings.instance()
        if cls._show_counter < plotly_settings.show_limit:
            # Increment the counter before invoking show (even if it does not succeed)
            cls._show_counter = cls._show_counter + 1
            # Show the figure if below the counter
            figure.show(*args, **kwargs)

