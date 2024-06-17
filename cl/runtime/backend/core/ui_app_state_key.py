# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from __future__ import annotations
from typing import final
from typing import Tuple
from typing import Type
from cl.runtime.backend.core.user_key import UserTable, UserKey
from cl.runtime.records.table_mixin import TableMixin


@final
class UiAppStateTable(TableMixin):
    """Table settings class."""

    @classmethod
    def create_key(cls, *, user: UserKey | str) -> UiAppStateKey:
        # TODO: Review if handling different parameter types is necessary
        if isinstance(user, tuple):
            return UiAppStateTable, user  # noqa
        elif isinstance(user, str):
            return UiAppStateTable, UserTable.create_key(username=user)
        else:
            raise RuntimeError(f"User key {user} is neither a tuple nor a string.")


UiAppStateKey = Tuple[Type[UiAppStateTable], UserKey]
