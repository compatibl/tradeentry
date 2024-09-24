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
from cl.runtime.settings.settings import Settings


@dataclass(slots=True, kw_only=True)
class PlotlySettings(Settings):
    """Settings for formatting and displaying Plotly plots."""

    show_limit: int = 0
    """Up to this number of plots will open in browser during a single test or __main__ session."""

    def __post_init__(self):
        """Perform validation and type conversions."""

        # Conversions
        if isinstance(self.show_limit, str) and self.show_limit.isdigit():
            self.max_test_plots = int(self.show_limit)

        if not isinstance(self.show_limit, int):
            raise RuntimeError(
                f"{type(self).__name__} field 'show_limit' must be"
                f"an int or a string that can be converted to an int."
            )

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_plotly"
