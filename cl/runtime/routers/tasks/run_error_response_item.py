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

from pydantic import BaseModel, Field


class RunErrorResponseItem(BaseModel):
    task_run_id: str
    """Task run id."""

    key: str
    """Key of the record."""

    name: str
    """Name of the exception."""

    status_code: int
    """Status code of the task."""

    message: str
    """Message of the exception."""

    stack_trace: str
    """Stack trace of the exception."""
