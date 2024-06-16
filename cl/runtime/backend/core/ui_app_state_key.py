# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.
from typing import Optional

from cl.runtime import Key, data_class, data_field
from cl.runtime.backend.core.user_key import UserKey


@data_class
class UiAppStateKey(Key):
    """Key for UiAppState class"""

    user: Optional[UserKey] = data_field()
    """A user the app state is applied for."""
