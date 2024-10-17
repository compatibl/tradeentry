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
from typing import Type

from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin
from cl.runtime.records.protocols import is_key


@dataclass(slots=True, kw_only=True)
class ApproverKey(KeyMixin):
    """Authorized approver."""

    approver_id: str = missing()
    """Unique approver identifier in 'LastName, FirstName' format."""
    
    def init(self) -> None:
        # Check only if inside a key, will be set automatically if inside a record
        if is_key(self):
            self.check_approver_id(self.approver_id)

    @classmethod
    def get_key_type(cls) -> Type:
        return ApproverKey

    @classmethod
    def get_approver_id(cls, *, first_name: str, last_name: str) -> str:
        """Create the unique identifier from parameters."""
        return f"{last_name}, {first_name}"

    @classmethod
    def check_approver_id(cls, approver_id: str) -> None:
        """Check that the unique identifier is compliant with the expected format."""
        if len(approver_id.split(", ")) != 2:
            raise UserError(
                f"Invalid ApproverId format: '{approver_id}', expected format is "
                f"'{{LastName}}, {{FirstName}}'"
            )
