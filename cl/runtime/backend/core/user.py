# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from typing import Optional

from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.storage.attrs import data_class, data_field


@data_class
class User(UserKey):
    """User which is allowed to log in."""

    first_name: str = data_field()
    """First name of the user."""

    last_name: str = data_field()
    """Last name of the user."""

    email: Optional[str] = data_field(default=None)
    """Email of the user."""
