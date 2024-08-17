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


@dataclass(slots=True, kw_only=True, frozen=True)
class DynaconfSettings(Settings):
    """Dynaconf system settings."""

    _root_path: str
    """Absolute path where Dynaconf settings file is found, use to define the location of project resources."""

    _loaded_files: str
    """List of loaded Dynaconf settings files."""

    @classmethod
    def get_prefix(cls) -> str | None:
        return None
