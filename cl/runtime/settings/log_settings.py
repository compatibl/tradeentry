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

import datetime as dt
from dataclasses import dataclass
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.settings.settings import Settings


@dataclass(slots=True, kw_only=True)
class LogSettings(Settings):
    """REST API settings."""

    filename_format: str = "prefix-timestamp"
    """
    Log filename format, the choices are:
    - prefix: Prefix only
    - prefix-timestamp: Prefix followed by UTC timestamp to millisecond precision in dash-delimited format
    """

    filename_prefix: str = "default"
    """Log filename prefix."""

    filename_timestamp: dt.datetime = DatetimeUtil.now()
    """Timestamp to use for log file, set to the time of program launch if not specified in settings."""

    level: str = "info"
    """Log level using logging module conventions (lower, upper or mixed case can be used)."""

    def __post_init__(self):
        """Perform validation and type conversions."""

        # Convert logging level to uppercase and validate its values
        self.level = self.level.upper()
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.level not in valid_levels:
            raise RuntimeError(
                f"Invalid log level: {self.level}, permitted values are: {', '.join(valid_levels)}. "
                f"Lower, upper or mixed case can be used."
            )

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_log"
