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

from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin
from dataclasses import dataclass
from typing import Type
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class TaskRunKey(KeyMixin):
    """
    The queue creates this record every time a task is submitted.

    Notes:
        - This record is periodically updated by the queue with the run status and result
        - This record must never be modified by the task itself
    """

    task_run_id: str = missing()  # TODO: Use UUID when fully supported
    """Time-ordered unique task run identifier in UUIDv7 string format."""

    @classmethod
    def get_key_type(cls) -> Type:
        return TaskRunKey
