# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.records.dataclasses_extensions import datafield
from cl.runtime.records.key_mixin import KeyMixin
from dataclasses import dataclass
from typing import Type


@dataclass(slots=True, kw_only=True)
class UiAppStateKey(KeyMixin):
    """UiAppState."""

    user: UserKey = datafield()
    """A user the app state is applied for."""

    def get_key_type(self) -> Type:
        return UiAppStateKey
