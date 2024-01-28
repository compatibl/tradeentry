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

from cl.runtime.data.dataclasses import data_class, data_field
from cl.runtime.storage.data_source import DataSource


@data_class
class DataSourceManager:
    """Manager class for creating a data source."""

    data_sources_config: str = data_field()
    """Name of configuration file."""

    data_sources_config_env: str = data_field()
    """Name of configuration environment."""

    default_host_name: str = data_field()
    """Default host name. Will be will be filled by update() method from config file."""

    def create_data_source(self) -> DataSource:
        """Create data source with default parameters."""
