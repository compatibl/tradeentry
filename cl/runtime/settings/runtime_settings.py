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

from cl.runtime.settings.settings import Settings
from dataclasses import dataclass
from typing import List


@dataclass(slots=True, kw_only=True, frozen=True)
class RuntimeSettings(Settings):
    """Runtime package settings."""

    load_packages: List[str]
    """List of packages to load in dot-delimited module prefix format, for example 'cl.runtime'."""

    api_host_name: str
    """REST API host name (either host name or IP can be used to access the API)."""

    api_host_ip: str
    """REST API host IP (either host name or IP can be used to access the API)."""

    api_port: int
    """REST API port."""

    data_source_class: str
    """Data source class in module.ClassName format."""

    data_source_id: str
    """Default data source identifier (the data source record must be loaded in code or from a csv/yaml/json file)."""

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_"
