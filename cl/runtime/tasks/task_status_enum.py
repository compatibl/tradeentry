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


class TaskStatusEnum(IntEnum):
    """
    Indicates task's progress from its initial Pending state through the Running and
    optionally Paused state and ending in one of Completed, Failed, or Cancelled states.
    """

    PENDING = 1
    """The task has been submitted to the queue but is not yet running."""

    RUNNING = 2
    """The task is running."""

    PAUSED = 3
    """The task is paused."""

    COMPLETED = 4
    """The task has been completed (successful completion)."""

    FAILED = 5
    """The task has failed (this status is distinct from 'Cancelled')."""

    CANCELLED = 6
    """The task has been cancelled (this status is distinct from 'Failed')."""
