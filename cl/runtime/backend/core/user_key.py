# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.key_mixin import KeyMixin
from dataclasses import dataclass
from typing import Type


@dataclass(slots=True, kw_only=True)
class UserKey(KeyMixin):
    """User which is allowed to log in."""

    username: str = field()
    """Unique user identifier."""

    def get_key_type(self) -> Type:
        return UserKey
