# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield
from cl.runtime.records.key_mixin import KeyMixin
from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True)
class UiAppStateKey(KeyMixin):
    """UiAppState."""

    user: UserKey = datafield()
    """A user the app state is applied for."""

    def get_generic_key(self) -> Tuple:
        return UiAppStateKey, self.user.get_generic_key()
