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

from enum import IntEnum


class LogEntryLevelEnum(IntEnum):
    """Indicates the type of event."""

    ERROR = 1
    """An error that prevents an application from functioning as expected."""

    WARNING = 2
    """An potential issue that could lead to problems."""

    USER_ERROR = 3
    """An error caused by incorrect user actions (invalid input, unauthorized access attempts, etc.)"""
