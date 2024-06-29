# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from dataclasses import dataclass
from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield
from cl.runtime.records.dataclasses.dataclass_key_mixin import DataclassKeyMixin
from cl.runtime.backend.core.user_key import UserKey


@dataclass(slots=True)
class UiAppStateKey(DataclassKeyMixin):
    """UiAppState."""

    user: UserKey = datafield()
    """A user the app state is applied for."""
