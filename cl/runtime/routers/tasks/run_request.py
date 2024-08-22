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


class RunRequest(BaseModel):
    """Request data type for the /tasks/run route."""

    user: str | None = Field(None)
    """User who triggered the task."""

    headers: dict[str, str] | None = Field(None)
    """Headers from the request."""

    data_source: str | None = Field(None)
    """Data source to be used."""

    dataset: str | None = Field(None)
    """Dataset to be used."""

    table: str | None = Field(None)
    """Type with the handler."""

    method: str | None = Field(None)
    """Method (handler) to be executed."""

    keys: list[str | None] | str | None = Field(None)
    """Keys to be used."""

    arguments_: dict[str, str] | None = Field(None, alias="arguments")
    """Arguments for the task."""

    data_: dict[str, str] | None = Field(None, alias="data")
    """Data for the data handler"""
