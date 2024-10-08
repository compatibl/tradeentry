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


class EntryStatusEnum(IntEnum):
    """Entry processing status."""

    COMPLETED = 1
    """Processing completed by AI or conventional code (excludes overrides and manual entries)."""

    ESCALATION = 2
    """Escalated by AI or conventional code for human review, contains pertinent details to create an override."""

    OVERRIDE = 3
    """Human override of a previously processed or escalated entry."""

    MANUAL = 4
    """New manual entry by a human in the normal course of processing (not an override)."""
