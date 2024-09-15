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

import logging
import os
from dataclasses import dataclass
from typing import Iterable
from concurrent_log_handler import ConcurrentRotatingFileHandler
from cl.runtime.log.log import Log
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.settings.log_settings import LogSettings
from cl.runtime.settings.settings import Settings


def _get_log_filename() -> str:
    """Generate log filename during import and use it throughout the session."""

    # Generate log file name
    log_settings = LogSettings.instance()
    log_filename_format = log_settings.filename_format
    match log_filename_format:
        case "prefix":
            # Filename is the prefix with .log extension
            result = f"{log_settings.filename_prefix}.log"
        case "prefix-timestamp":
            # UTC timestamp to millisecond precision for the log file name
            log_timestamp = DatetimeUtil.now()
            # Serialize assuming millisecond precision
            log_timestamp_str = (
                log_timestamp.strftime("%Y-%m-%d-%H-%M-%S") + f"-{int(round(log_timestamp.microsecond / 1000)):03d}"
            )
            result = f"{log_settings.filename_prefix}-{log_timestamp_str}.log"
        case _:
            valid_choices = ["prefix", "prefix-timestamp"]
            raise RuntimeError(
                f"Unknown log filename format: {log_filename_format}, " f"valid choices are {', '.join(valid_choices)}"
            )

    # Create log directory and filename relative to project root
    project_root = Settings.get_project_root()
    log_dir = os.path.join(project_root, "logs")
    result = os.path.join(log_dir, result)

    # Create log directory if does not exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    return result


log_filename = _get_log_filename()
"""Generate log filename during import and use it throughout the session."""


@dataclass(slots=True, kw_only=True)
class FileLog(Log):
    """File log with concurrency multiprocess write capability."""

    filename: str = log_filename
    """Log filename with extension is generated on import."""

    def get_log_handlers(self) -> Iterable[logging.Handler]:
        """Return an iterable of log handlers to be added to the logger."""

        # Max log file in bytes, after this size is reached older records will be erased
        max_log_file_size_bytes = 1024 * 1024 * 10  # 10MB

        # Set up file handler
        file_log_handler = ConcurrentRotatingFileHandler(
            self.filename,
            maxBytes=max_log_file_size_bytes,
            backupCount=0,  # Do not create backup files because each file has a timestamp
        )

        # Configure the logging format
        file_log_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(custom_field)s"
        )
        file_log_handler.setFormatter(file_log_formatter)

        # TODO: Add another handler that saves records
        return [file_log_handler]
