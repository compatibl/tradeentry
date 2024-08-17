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

from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.settings.settings import Settings
from dataclasses import dataclass
from typing import List


@dataclass(slots=True, kw_only=True)
class ContextSettings(Settings):
    """Runtime context settings specifies default context parameters."""

    packages: List[str]
    """List of packages to load in dot-delimited module prefix format, for example 'cl.runtime'."""

    data_source_class: str  # TODO: Deprecated, switch to preloaded class
    """Data source class in module.ClassName format."""

    data_source: str
    """Default data source identifier (the data source record must be loaded in code or from a csv/yaml/json file)."""

    def __post_init__(self):
        """Perform validation and type conversions."""

        # TODO: Move to ValidationUtil or PrimitiveUtil class
        if isinstance(self.packages, list):
            pass
        elif self.packages is None:
            self.packages = []
        elif isinstance(self.packages, str):
            self.packages = [self.packages]
        elif hasattr(self.packages, "__iter__"):
            self.packages = list(self.packages)
        else:
            raise RuntimeError(f"{type(self).__name__} field 'packages' must be a string or an iterable of strings.")

        if isinstance(self.data_source, str):
            pass
        else:
            raise RuntimeError(f"{type(self).__name__} field 'data_source' must be a string.")

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_context"
