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

import os
from dataclasses import dataclass
from getpass import getuser
from typing_extensions import Self
from cl.runtime import Context
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.workflows.approver_key import ApproverKey

_os_dict = None
"""Dictionary by OS token."""

_auth_dic = None
"""Dictionary by authorization token."""


@dataclass(slots=True, kw_only=True)
class Approver(ApproverKey, RecordMixin[ApproverKey]):
    """Approver which is allowed to log in."""

    first_name: str = missing()
    """First name of the approver (part of approver_id)."""

    last_name: str = missing()
    """Last name of the approver (part of approver_id)."""

    email: str | None = None
    """Email of the approver."""

    username_ad: str | None = None
    """Approver token returned by OS."""

    username_okta: str | None = None
    """Approver token returned by auth."""

    def init(self) -> None:
        # Generate from fields
        self.approver_id = ApproverKey.get_approver_id(first_name=self.first_name, last_name=self.last_name)

    def get_key(self) -> ApproverKey:
        return ApproverKey(approver_id=self.approver_id)

    @classmethod
    def current(cls) -> ApproverKey:
        """Get from token in any format (auth first, then OS)."""
        global _os_dict
        global _auth_dict
        # Populate dicts if not defined
        if _os_dict is None or _auth_dict is None:
            _os_dict = {}
            _auth_dict = {}
            context = Context.current()
            approvers = context.load_all(Approver)
            for approver in approvers:
                if approver.username_ad is not None:
                    _os_dict[approver.username_ad] = approver.get_key()
                if approver.username_okta is not None:
                    _auth_dict[approver.username_okta] = approver.get_key()

        # Look up by auth token on Linux and OS token on Windows
        # TODO: Make approver lookup based on Dynaconf settings, not OS
        result = None
        if os.name == "nt":
            token = getuser()
            result = _os_dict.get(token, None)
        else:
            raise UserError("Authorization required for configuring the list of Approvers.")
            token = None  # TODO: Get from auth
            result = _auth_dict.get(token, None)

        if result is None:
            raise UserError(f"Approver role is not configured for the current user.")
        return result
