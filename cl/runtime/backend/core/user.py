# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.records.dataclasses_extensions import field, missing
from cl.runtime.records.record_mixin import RecordMixin
from dataclasses import dataclass


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
