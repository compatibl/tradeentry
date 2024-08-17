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
from pathlib import Path

from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.settings.settings import Settings
from dataclasses import dataclass
from typing import List


@dataclass(slots=True, kw_only=True)
class DynaconfSettings(Settings):
    """Dynaconf system settings."""

    settings_file: List[str]
    """List of Dynaconf settings file patterns or file paths."""

    _root_path: str
    """Absolute path where Dynaconf settings file is found, use to define the location of project resources."""

    _loaded_files: str
    """List of loaded Dynaconf settings files."""

    def __post_init__(self):
        """Perform validation and type conversions."""

        # TODO: Move to ValidationUtil or PrimitiveUtil class
        if isinstance(self.settings_file, list):
            pass
        elif self.settings_file is None:
            self.settings_file = []
        elif isinstance(self.settings_file, str):
            self.settings_file = [self.settings_file]
        elif hasattr(self.settings_file, '__iter__'):
            self.settings_file = list(self.settings_file)
        else:
            raise RuntimeError("Dynaconf settings_file field must be a string or an iterable of strings.")

        if isinstance(self._root_path, str):
            pass
        elif self._root_path is None:
            pass
        elif isinstance(self._root_path, Path):
            self._root_path = str(self._root_path)
        else:
            raise RuntimeError("Dynaconf _root_path field must be a string or Path.")

    @classmethod
    def get_prefix(cls) -> str | None:
        return None
