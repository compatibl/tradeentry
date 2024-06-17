# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from __future__ import annotations
from typing import final
from typing import Tuple
from typing import Type
from cl.runtime.records.table_mixin import TableMixin


@final
class UserTable(TableMixin):
    """Table settings class."""

    @classmethod
    def create_key(cls, *, username: str) -> UserKey:
        return UserTable, username


UserKey = Tuple[Type[UserTable], str]

