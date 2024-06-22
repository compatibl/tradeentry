# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from dataclasses import dataclass
from typing import List, Optional, final
from cl.runtime.backend.core.ui_type_state_key import UiTypeStateKey
from cl.runtime.records.dataclasses.dataclass_record_mixin import datafield


@final
@dataclass(slots=True, kw_only=True)
class UiTypeState(UiTypeStateKey):
    """Defines ui settings for a type."""

    read_only: Optional[bool] = datafield()
    """Specifies if records of this type are readonly."""

    use_cache: Optional[bool] = datafield()
    """
    If set and TRUE data will be cached until tab is opened. This means that the next time the tab is
    activated, the main grid data request will not be submitted, it will be taken from the browser cache.
    """

    pinned_handlers: Optional[List[str]] = datafield()
    """List of names of the handlers pinned for the type"""
