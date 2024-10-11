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

from dataclasses import dataclass
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin


@dataclass(slots=True, kw_only=True)
class User(UserKey, RecordMixin[UserKey]):
    """User which is allowed to log in."""

    first_name: str = missing()
    """First name of the user."""

    last_name: str = missing()
    """Last name of the user."""

    email: str | None = None
    """Email of the user."""

    def get_key(self) -> UserKey:
        return UserKey(username=self.username)

    def init(self) -> None:
        """Generate username in 'LastName, FirstName' format if not specified and check if specified."""
        username = f"{self.last_name}, {self.first_name}"
        if self.username is None:
            # Assign if not specified
            self.username = username
        elif self.username != username:
            # Otherwise check that it matches the rest of the data
            raise RuntimeError(
                f"Username {self.username} is not in 'LastName, FirstName' format for last name "
                f"'{self.last_name}' and first name '{self.last_name}'."
            )
