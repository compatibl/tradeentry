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
    """Default context parameters."""

    packages: List[str]
    """List of packages to load in dot-delimited format, for example 'cl.runtime' or 'stubs.cl.runtime'."""

    log_class: str = "cl.runtime.log.file.file_log.FileLog"  # TODO: Deprecated, switch to class-specific fields
    """Default log class in module.ClassName format."""

    db_class: str  # TODO: Deprecated, switch to class-specific fields
    """Default database class in module.ClassName format."""

    db_id: str
    """Default database identifier, if 'db_class' is a key it will be obtained from preloads."""

    db_temp_prefix: str = "temp;"
    """
    IMPORTANT: DELETING ALL RECORDS AND DROPPING THE DATABASE FROM CODE IS PERMITTED
    when both db_id and database name start with this prefix.
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
        if not isinstance(self.db_class, str):
            raise RuntimeError(
                f"{type(self).__name__} field 'db_class' must be a string " f"in module.ClassName format."
            )
        if not isinstance(self.db_id, str):
            raise RuntimeError(f"{type(self).__name__} field 'context_id' must be a string.")

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_context"
