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

from cl.runtime.primitive.datetime_util import DatetimeUtil
from concurrent_log_handler import ConcurrentRotatingFileHandler
from cl.runtime.settings.log_settings import LogSettings
from cl.runtime.settings.settings import Settings

# Get log settings
log_settings = LogSettings.instance()

# Generate log file name with the timestamp
timestamp = DatetimeUtil.now()
timestamp_str = timestamp.strftime("%Y-%m-%d-%H-%M-%S") + f"-{int(round(timestamp.microsecond / 1000)):03d}"
log_filename = f"runtime-{timestamp_str}.log"
project_root = Settings.get_project_root()
log_dir = os.path.join(project_root, "logs")
log_file = os.path.join(log_dir, log_filename)

# Create log directory if does not exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up file handler
log_handler = ConcurrentRotatingFileHandler(
    log_file,
    maxBytes=1024*1024*10,  # Max size of 10mb per timestamped log file
    backupCount=0           # Do not create backup files because each file has a timestamp
)

# Configure the logging format
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(custom_field)s')
log_handler.setFormatter(log_formatter)


class LogFilter(logging.Filter):
    """Logging filter adds custom fields to log messages."""
    def filter(self, record):
        record.custom_field = "custom_field_value"
        return True
