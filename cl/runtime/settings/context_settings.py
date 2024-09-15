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
from typing import List
from cl.runtime.settings.settings import Settings


@dataclass(slots=True, kw_only=True)
class ContextSettings(Settings):
    """Runtime context settings specifies default context parameters."""

    packages: List[str]
    """List of packages to load in dot-delimited module prefix format, for example 'cl.runtime'."""

    log_class: str = "cl.runtime.log.file.file_log.FileLog"  # TODO: Deprecated, switch to class-specific fields
    """Default log class in module.ClassName format."""

    data_source_class: str  # TODO: Deprecated, switch to class-specific fields
    """Default data source class in module.ClassName format."""

    data_source_id: str
    """Default data source identifier, if 'data_source_class' is a key it will be obtained from preloads."""

    data_source_temp_db_prefix: str = "temp;"
    """
    IMPORTANT: DELETING ALL RECORDS AND DROPPING THE DATABASE FROM CODE IS PERMITTED
    when both data_source_id and database name start with this prefix.
    """

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

        if not isinstance(self.log_class, str):
            raise RuntimeError(
                f"{type(self).__name__} field 'log_class' must be a string " f"in module.ClassName format."
            )
        if not isinstance(self.data_source_class, str):
            raise RuntimeError(
                f"{type(self).__name__} field 'data_source_class' must be a string " f"in module.ClassName format."
            )
        if not isinstance(self.data_source_id, str):
            raise RuntimeError(f"{type(self).__name__} field 'context_id' must be a string.")

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_context"
