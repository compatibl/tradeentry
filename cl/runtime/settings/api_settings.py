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
class ApiSettings(Settings):
    """Runtime REST API settings."""

    host_name: str = "localhost"
    """REST API host name (either host name or IP can be used to access the API)."""

    host_ip: str = "127.0.0.1"
    """REST API host IP (either host name or IP can be used to access the API)."""

    port: int = 7008
    """REST API port."""

    def __post_init__(self):
        """Perform validation and type conversions."""

        if not isinstance(self.host_name, str):
            raise RuntimeError(f"{type(self).__name__} field 'host_name' must be a string.")
        if not isinstance(self.host_ip, str):
            raise RuntimeError(f"{type(self).__name__} field 'host_ip' must be a string.")

        if isinstance(self.port, int):
            pass
        elif isinstance(self.port, str):
            if self.port.isdigit():
                self.port = int(self.port)
            else:
                raise RuntimeError(f"{type(self).__name__} field 'port' includes non-digit characters.")
        else:
            raise RuntimeError(f"{type(self).__name__} field 'port' must be an int or a string.")

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_api"
