# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield
from cl.runtime.records.dataclasses.dataclass_key_mixin import DataclassKeyMixin
from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True)
class UserKey(DataclassKeyMixin):
    """User which is allowed to log in."""

    username: str = datafield()
    """Unique user identifier."""

    def get_generic_key(self) -> Tuple:
        return UserKey, self.username
