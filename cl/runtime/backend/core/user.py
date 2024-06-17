# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from dataclasses import dataclass

from cl.runtime.backend.core.user_key import UserKey, UserTable
from cl.runtime.records.dataclasses.dataclass_mixin import datafield, DataclassMixin


@dataclass(slots=True, kw_only=True)
class User(DataclassMixin):
    """User which is allowed to log in."""

    username: str = datafield()
    """Unique user identifier."""

    first_name: str = datafield()
    """First name of the user."""

    last_name: str = datafield()
    """Last name of the user."""

    email: str | None = datafield(default=None)
    """Email of the user."""

    def get_key(self) -> UserKey:
        return UserTable, self.username
