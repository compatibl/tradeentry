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

from abc import abstractmethod, ABC
from dataclasses import dataclass

from cl.convince.entries.entry_type_key import EntryTypeKey
from cl.runtime import Context
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.convince.entries.entry_key import EntryKey


@dataclass(slots=True, kw_only=True)
class Entry(EntryKey, RecordMixin[EntryKey], ABC):
    """Contains title, body and supporting data of user entry along with the entry processing result."""

    title: str = missing()
    """Title of a long entry or complete description of a short one (included in MD5 hash)."""

    body: str | None = None
    """Optional body of the entry if not completely described by the title (included in MD5 hash)."""

    data: str | None = None
    """Optional supporting data in YAML format (included in MD5 hash)."""

    approved_by: UserKey | None = None
    """User who recorded the approval."""

    few_shot: bool | None = None
    """If True, use this entry as a few-shot example."""

    def get_key(self) -> EntryKey:
        return EntryKey(entry_id=self.entry_id)

    def init(self) -> None:
        """Generate entry_id in 'type: title' format followed by an MD5 hash of body and data if present."""
        # Convert field types if necessary
        if self.few_shot is not None and isinstance(self.few_shot, str):
            self.few_shot = self.parse_optional_bool(self.few_shot, field_name="few_shot")
        # Record type is part of the key
        record_type = type(self).__name__
        self.entry_id = self.get_entry_id(record_type, self.title, self.body, self.data)

    # TODO: Restore abstract when implemented @abstractmethod
    def run_propose(self) -> None:
        """Generate or regenerate the proposed value."""

    def run_approve(self) -> None:  # TODO: Review
        """Approve the manually set approved value, or proposed value if the approved value is not set."""
        # Set approved_py to the user obtained from the current context and save
        context = Context.current()
        self.approved_by = context.user
        context.save_one(self)

    @classmethod
    def parse_required_bool(cls, field_value: str | None, *, field_name: str | None = None) -> bool:  # TODO: Move to Util class
        """Parse an optional boolean value."""
        match field_value:
            case None | "":
                field_name = CaseUtil.snake_to_pascal_case(field_name)
                for_field = f"for field {field_name}" if field_name is not None else " for a Y/N field"
                raise UserError(f"The value {for_field} is empty. Valid values are Y or N.")
            case "Y":
                return True
            case "N":
                return False
            case _:
                field_name = CaseUtil.snake_to_pascal_case(field_name)
                for_field = f" for field {field_name}" if field_name is not None else  " for a Y/N field"
                raise UserError(f"The value {for_field} must be Y, N or an empty string.\nField value: {field_value}")

    @classmethod
    def parse_optional_bool(cls, field_value: str | None, *, field_name: str | None = None) -> bool | None:  # TODO: Move to Util class
        """Parse an optional boolean value."""
        match field_value:
            case None | "":
                return None
            case "Y":
                return True
            case "N":
                return False
            case _:
                field_name = CaseUtil.snake_to_pascal_case(field_name)
                for_field = f" for field {field_name}" if field_name is not None else ""
                raise UserError(f"The value{for_field} must be Y, N or an empty string.\nField value: {field_value}")
