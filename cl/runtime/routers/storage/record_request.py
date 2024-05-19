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

from cl.runtime.routers.user_request import UserRequest


class RecordRequest(UserRequest):
    """Request data type for the /storage/record route."""

    type_: str
    """Class name."""

    # TODO: Check if it should be made optional for singletons
    key: str
    """Primary key fields in semicolon-delimited format."""

    module: str | None = None
    """Dot-delimited module string."""

    dataset: str | None = None
    """Dataset string."""

    ignore_record_absence: bool = False
    """If true, empty response will be returned without error if the record is not found."""
