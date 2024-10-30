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

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from cl.runtime import Context
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.convince.entries.entry_key import EntryKey


@dataclass(slots=True, kw_only=True)
class Entry(EntryKey, RecordMixin[EntryKey], ABC):
    """Contains description, body and supporting data of user entry along with the entry processing result."""

    description: str = missing()
    """Description exactly as provided by the user (included in MD5 hash)."""

    body: str | None = None
    """Optional text following the description exactly as provided by the user (included in MD5 hash)."""

    data: str | None = None
    """Optional supporting data in YAML format (included in MD5 hash)."""

    lang: str | None = "en"
    """ISO 639-1 two-letter lowercase language code (defaults to 'en')."""

    verified: bool | None = None
    """If True, use this entry as a few-shot sample."""

    def get_key(self) -> EntryKey:
        return EntryKey(entry_id=self.entry_id)

    def init(self) -> None:
        """Generate entry_id in 'type: description' format followed by an MD5 hash of body and data if present."""
        # Convert field types if necessary
        if self.verified is not None and isinstance(self.verified, str):
            self.verified = self.parse_optional_bool(self.verified, field_name="verified")
        # Record type is part of the key
        record_type = type(self).__name__
        self.entry_id = self.get_entry_id(record_type, self.description, self.body, self.data)

    def get_text(self) -> str:
        """Get the complete text of the entry."""
        # TODO: Support body and data
        if self.body is not None:
            raise RuntimeError("Entry 'body' field is not yet supported.")
        if self.data is not None:
            raise RuntimeError("Entry 'data' field is not yet supported.")
        result = self.description
        return result

    # TODO: Restore abstract when implemented for all entries
    def run_propose(self) -> None:
        """Generate or regenerate the proposed value."""
        raise UserError(f"Propose handler is not yet implemented for {type(self).__name__}.")

    def run_reset(self) -> None:
        """Clear all output  fields and verification flag."""
        record_type = type(self)
        result = record_type(
            description=self.description,
            body=self.body,
            data=self.data,
            lang=self.lang,
        )
        Context.current().save_one(result)

    def run_mark_verified(self) -> None:
        """Mark verified."""
        self.verified = True
        Context.current().save_one(self)

    def run_unmark_verified(self) -> None:
        """Unmark verified."""
        self.verified = False
        Context.current().save_one(self)

    @classmethod
    def parse_required_bool(
        cls, field_value: str | None, *, field_name: str | None = None
    ) -> bool:  # TODO: Move to Util class
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
                for_field = f" for field {field_name}" if field_name is not None else " for a Y/N field"
                raise UserError(f"The value {for_field} must be Y, N or an empty string.\nField value: {field_value}")

    @classmethod
    def parse_optional_bool(
        cls, field_value: str | None, *, field_name: str | None = None
    ) -> bool | None:  # TODO: Move to Util class
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
