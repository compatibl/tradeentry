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
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar
from typing import Iterable
from typing_extensions import Self
from cl.runtime.log.log_filter import LogFilter
from cl.runtime.log.log_key import LogKey
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.settings.context_settings import ContextSettings
from cl.runtime.settings.log_settings import LogSettings


@dataclass(slots=True, kw_only=True)
class Log(LogKey, RecordMixin[LogKey], ABC):
    """A target for log messages."""

    # TODO: Do not store here, instead get from settings once during the initial Context construction
    __default: ClassVar[Self | None] = None

    level: str = LogSettings.instance().level
    """Log level using logging module conventions (lower, upper or mixed case can be used)."""

    def get_key(self) -> LogKey:
        return LogKey(log_id=self.log_id)

    @classmethod
    def default(cls) -> Self:
        """Default log is initialized from settings and cannot be modified in code."""

        if Log.__default is None:
            # Create the class specified in settings and invoke its constructor
            context_settings = ContextSettings.instance()
            log_type = ClassInfo.get_class_type(context_settings.log_class)
            Log.__default = log_type()

        return Log.__default

    def get_logger(self, name: str) -> logging.Logger:
        """Get logger for the specified name, invoke with __name__ as the argument."""

        # Create logger and add filter for custom fields
        logger = logging.getLogger(name)
        logger.addFilter(LogFilter())

        # Set level
        logger.setLevel(self.level)

        # Add handlers
        log_handlers = self.get_log_handlers()
        [logger.addHandler(log_handler) for log_handler in log_handlers]

        return logger

    @abstractmethod
    def get_log_handlers(self) -> Iterable[logging.Handler]:
        """Return an iterable of log handlers to be added to the logger."""
