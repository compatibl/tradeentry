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


@dataclass(slots=True, kw_only=True)
class FireworksSettings(Settings):
    """Fireworks settings."""

    api_key: str
    """Fireworks API key."""

    def __post_init__(self):
        """Perform validation and type conversions."""

        if not isinstance(self.api_key, str):
            raise RuntimeError(f"{type(self).__name__} field 'api_key' must be a string.")

    @classmethod
    def get_prefix(cls) -> str:
        return "fireworks"
